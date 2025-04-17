#include <thread>
#include <atomic>
#include <chrono>
#include <vector>
#include <iostream>
#include <windows.h>
#include <opencv2/opencv.hpp>
#include "SharedMemory.h"

const struct CaptureRegion
{
    int x, y, width, height;
} SERVE_REGION = {844, 866, 1, 1}, TOSS_REGION = {956, 1050, 1, 1};

const struct Color
{
    int r, g, b;
} SERVE_COLOR = {194, 213, 223}, TOSS_COLOR = {229, 164, 93};

class ScreenCapture
{
private:
    HWND hwnd;
    HDC hWindowDC;
    HDC hMemoryDC;
    HBITMAP hBitmap;

public:
    ScreenCapture(HWND hwnd, int width, int height) : hwnd(hwnd), hWindowDC(nullptr), hMemoryDC(nullptr), hBitmap(nullptr)
    {
        if (!hwnd)
            return;

        hWindowDC = GetDC(hwnd);
        if (!hWindowDC)
            return;

        hMemoryDC = CreateCompatibleDC(hWindowDC);
        hBitmap = CreateCompatibleBitmap(hWindowDC, width, height);
        SelectObject(hMemoryDC, hBitmap);
    }

    ~ScreenCapture()
    {
        if (hBitmap)
            DeleteObject(hBitmap);
        if (hMemoryDC)
            DeleteDC(hMemoryDC);
        if (hWindowDC && hwnd)
            ReleaseDC(hwnd, hWindowDC);
    }

    cv::Mat capture(int x, int y, int width, int height)
    {
        if (!hWindowDC || !hMemoryDC)
            return cv::Mat();

        BitBlt(hMemoryDC, 0, 0, width, height, hWindowDC, x, y, SRCCOPY);
        BITMAPINFOHEADER bi = {sizeof(BITMAPINFOHEADER), width, -height, 1, 32, BI_RGB};
        std::vector<unsigned char> buffer(width * height * 4);
        GetDIBits(hMemoryDC, hBitmap, 0, height, buffer.data(), (BITMAPINFO *)&bi, DIB_RGB_COLORS);

        cv::Mat img(height, width, CV_8UC4, buffer.data());
        cv::Mat bgr;
        cv::cvtColor(img, bgr, cv::COLOR_BGRA2BGR);
        return bgr;
    }
};

static HWND getRobloxWindow()
{
    HWND robloxHwnd = FindWindow(NULL, L"Roblox");
    return (robloxHwnd && GetForegroundWindow() == robloxHwnd) ? robloxHwnd : nullptr;
}

static bool checkPixelColor(const cv::Mat &img, const Color &targetColor)
{
    if (img.empty())
        return false;

    cv::Vec3b pixel = img.at<cv::Vec3b>(0, 0);
    return pixel[2] == targetColor.r &&
           pixel[1] == targetColor.g &&
           pixel[0] == targetColor.b;
}

static void serveLoop(SharedMemory &shm, std::atomic<bool> &running)
{
    while (running && shm.getBool(ShmVariable::isServing))
    {
        shm.setBool(ShmVariable::isInServeLoop, true);

        HWND robloxHwnd = getRobloxWindow();
        if (!robloxHwnd)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            continue;
        }

        ScreenCapture capture(robloxHwnd, SERVE_REGION.width, SERVE_REGION.height);
        cv::Mat screenshot = capture.capture(SERVE_REGION.x, SERVE_REGION.y,
                                             SERVE_REGION.width, SERVE_REGION.height);

        if (checkPixelColor(screenshot, SERVE_COLOR))
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(480));
            shm.setBool(ShmVariable::serveCommand, true);
            shm.setBool(ShmVariable::isInServeLoop, false);
            break;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    shm.setBool(ShmVariable::isInServeLoop, false);
}

static void tossLoop(SharedMemory &shm, std::atomic<bool> &running)
{
    while (running)
    {
        HWND robloxHwnd = getRobloxWindow();
        if (!robloxHwnd)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            continue;
        }

        ScreenCapture capture(robloxHwnd, TOSS_REGION.width, TOSS_REGION.height);
        cv::Mat screenshot = capture.capture(TOSS_REGION.x, TOSS_REGION.y,
                                             TOSS_REGION.width, TOSS_REGION.height);

        if (checkPixelColor(screenshot, TOSS_COLOR))
        {
            shm.setBool(ShmVariable::isServing, true);
            if (!shm.getBool(ShmVariable::isInServeLoop))
            {
                std::thread(serveLoop, std::ref(shm), std::ref(running)).detach();
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

        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

int main()
{
    SharedMemory shm;
    if (!shm.initialize())
    {
        std::cerr << "Shared memory initialization failed!" << std::endl;
        return 1;
    }

    std::atomic<bool> running(true);
    try
    {
        tossLoop(shm, running);
    }
    catch (const std::exception &e)
    {
        std::cerr << "Exception occurred: " << e.what() << std::endl;
        running = false;
        return 1;
    }

    return 0;
}