#include <thread>
#include <atomic>
#include <chrono>
#include <vector>
#include <iostream>
#include <windows.h>
#include "SharedMemory.h"
#include <opencv2/opencv.hpp>

const double THRESHOLD = 0.9;

cv::Mat tossImg = cv::imread("assets/1920x1080/normal/toss.png", cv::IMREAD_COLOR);
cv::Mat serveImg = cv::imread("assets/1920x1080/normal/serve.png", cv::IMREAD_COLOR);

static bool checkTemplatesLoaded()
{
    if (tossImg.empty() || serveImg.empty())
    {
        std::cerr << "One or both template images not found!" << std::endl;
        return false;
    }
    return true;
}

static HWND getRobloxWindow()
{
    HWND robloxHwnd = FindWindow(NULL, L"Roblox");
    HWND activeHwnd = GetForegroundWindow();
    if (robloxHwnd && activeHwnd == robloxHwnd)
    {
        return robloxHwnd;
    }
    return NULL;
}

static bool getRobloxWindowRect(int &left, int &top, int &width, int &height)
{
    HWND robloxHwnd = FindWindow(NULL, L"Roblox");
    if (!robloxHwnd)
    {
        std::cerr << "Roblox window not found!" << std::endl;
        return false;
    }
    RECT rect;
    if (!GetWindowRect(robloxHwnd, &rect))
    {
        std::cerr << "Failed to get window rect: " << GetLastError() << std::endl;
        return false;
    }
    left = rect.left;
    top = rect.top;
    width = rect.right - rect.left;
    height = rect.bottom - rect.top;
    return true;
}

static cv::Mat captureRegion(HWND hwnd, int x, int y, int width, int height)
{
    if (!hwnd)
        return cv::Mat();
    HDC hWindowDC = GetDC(hwnd);
    if (!hWindowDC)
        return cv::Mat();
    HDC hMemoryDC = CreateCompatibleDC(hWindowDC);
    HBITMAP hBitmap = CreateCompatibleBitmap(hWindowDC, width, height);
    SelectObject(hMemoryDC, hBitmap);
    BitBlt(hMemoryDC, 0, 0, width, height, hWindowDC, x, y, SRCCOPY);
    BITMAPINFOHEADER bi = {sizeof(BITMAPINFOHEADER), width, -height, 1, 32, BI_RGB};
    std::vector<unsigned char> buffer(width * height * 4);
    GetDIBits(hMemoryDC, hBitmap, 0, height, buffer.data(), (BITMAPINFO *)&bi, DIB_RGB_COLORS);
    cv::Mat img(height, width, CV_8UC4, buffer.data());
    cv::Mat bgr;
    cv::cvtColor(img, bgr, cv::COLOR_BGRA2BGR);
    DeleteObject(hBitmap);
    DeleteDC(hMemoryDC);
    ReleaseDC(hwnd, hWindowDC);
    return bgr;
}

static void serveLoop(SharedMemory &shm)
{
    while (true)
    {
        shm.setBool(ShmVariable::isInServeLoop, true);
        if (!shm.getBool(ShmVariable::isServing))
        {
            shm.setBool(ShmVariable::isInServeLoop, false);
            break;
        }
        HWND robloxHwnd = getRobloxWindow();
        int left, top, width, height;
        if (robloxHwnd && getRobloxWindowRect(left, top, width, height))
        {
            // cv::Mat screenshot = captureRegion(robloxHwnd, 854, 849, 193, 13);
            cv::Mat screenshot = captureRegion(robloxHwnd, 854, 849, 13, 13);
            // cv::Mat screenshot = captureRegion(robloxHwnd, left, top, width, height);
            // std::cout << left << " " << top << " " << width << " " << height << std::endl;
            if (!screenshot.empty())
            {
                cv::Mat result;
                cv::matchTemplate(screenshot, serveImg, result, cv::TM_CCOEFF_NORMED);
                double maxVal;
                cv::Point maxLoc;
                cv::minMaxLoc(result, nullptr, &maxVal, nullptr, &maxLoc);
                if (maxVal >= 0.9)
                {
                    // std::cout << "FOUND" << std::endl;
                    // std::cout << "Serve detected at: " << maxLoc.x << ", " << maxLoc.y << ", " << serveImg.cols << ", " << serveImg.rows << " " << maxVal << std::endl;
                    std::this_thread::sleep_for(std::chrono::milliseconds(500));
                    shm.setBool(ShmVariable::serveCommand, true);
                    shm.setBool(ShmVariable::isInServeLoop, false);
                    break;
                }
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}

static void tossLoop(SharedMemory &shm)
{
    while (true)
    {
        HWND robloxHwnd = getRobloxWindow();
        int left, top, width, height;
        if (robloxHwnd && getRobloxWindowRect(left, top, width, height))
        {
            cv::Mat screenshot = captureRegion(robloxHwnd, 918, 1050, 74, 11);
            if (!screenshot.empty())
            {
                cv::Mat result;
                cv::matchTemplate(screenshot, tossImg, result, cv::TM_CCOEFF_NORMED);
                double maxVal;
                cv::Point maxLoc;
                cv::minMaxLoc(result, nullptr, &maxVal, nullptr, &maxLoc);
                if (maxVal >= THRESHOLD)
                {
                    shm.setBool(ShmVariable::isServing, true);
                    if (!shm.getBool(ShmVariable::isInServeLoop))
                    {
                        std::thread(serveLoop, std::ref(shm)).detach();
                    }
                }
                else
                {
                    shm.setBool(ShmVariable::isInServeLoop, false);
                    shm.setBool(ShmVariable::isServing, false);
                    shm.setBool(ShmVariable::isServe, false);
                    shm.setBool(ShmVariable::isToss, false);
                    shm.setBool(ShmVariable::serveCommand, false);
                }
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}

int main()
{
    SharedMemory shm;
    if (!checkTemplatesLoaded())
        return 1;
    if (!shm.initialize())
        return 1;
    tossLoop(shm);
    return 0;
}