#include <string>
#include <windows.h>
#include "SharedMemory.h"

namespace OverlayConfig
{
    const int WIDTH = 800;
    const int HEIGHT = 600;
    const int OFFSET_X = 100;
    const int OFFSET_Y = 100;
    const std::string TITLE = "Volleyball Legends Pro";
    const int TEXT_HEIGHT = 50;
    const int UPDATE_INTERVAL_MS = 100;
    const COLORREF BG_COLOR = RGB(255, 255, 255);
    const COLORREF LINE_COLOR = RGB(255, 0, 0);
    const COLORREF TEXT_ACTIVE_COLOR = RGB(0, 255, 0);
    const COLORREF TEXT_INACTIVE_COLOR = RGB(255, 0, 0);
}

class GDIResource
{
private:
    HFONT hFont;

public:
    GDIResource() : hFont(nullptr)
    {
        hFont = CreateFontA(
            OverlayConfig::TEXT_HEIGHT,
            0, 0, 0,
            FW_NORMAL,
            FALSE, FALSE, FALSE,
            ANSI_CHARSET,
            OUT_DEFAULT_PRECIS,
            CLIP_DEFAULT_PRECIS,
            DEFAULT_QUALITY,
            DEFAULT_PITCH | FF_DONTCARE,
            "Arial");
    }

    ~GDIResource()
    {
        if (hFont)
            DeleteObject(hFont);
    }

    HFONT getFont() const { return hFont; }
};

struct OverlayState
{
    HWND overlayHwnd;
    int lineX;
    int serveTextX, serveTextY;
    std::string serveText;
    COLORREF textColor;
    bool showLine;
    bool showText;
    SharedMemory shm;
    GDIResource gdi;
};

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static OverlayState *state = nullptr;

    switch (uMsg)
    {
    case WM_CREATE:
    {
        state = static_cast<OverlayState *>(((CREATESTRUCT *)lParam)->lpCreateParams);
        SetTimer(hwnd, 1, OverlayConfig::UPDATE_INTERVAL_MS, NULL);
        return 0;
    }
    case WM_PAINT:
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);

        RECT rect;
        GetClientRect(hwnd, &rect);

        HDC hdcMem = CreateCompatibleDC(hdc);
        HBITMAP hbmMem = CreateCompatibleBitmap(hdc, rect.right, rect.bottom);
        HBITMAP hbmOld = (HBITMAP)SelectObject(hdcMem, hbmMem);

        HBRUSH hBrush = CreateSolidBrush(OverlayConfig::BG_COLOR);
        FillRect(hdcMem, &rect, hBrush);
        DeleteObject(hBrush);

        if (state->showLine)
        {
            HPEN hPen = CreatePen(PS_SOLID, 1, OverlayConfig::LINE_COLOR);
            SelectObject(hdcMem, hPen);
            MoveToEx(hdcMem, state->lineX, 0, NULL);
            LineTo(hdcMem, state->lineX, rect.bottom / 2);
            DeleteObject(hPen);
        }

        if (state->showText)
        {
            HFONT hOldFont = (HFONT)SelectObject(hdcMem, state->gdi.getFont());
            SetTextColor(hdcMem, state->textColor);
            SetBkMode(hdcMem, TRANSPARENT);
            TextOutA(hdcMem, state->serveTextX, state->serveTextY,
                     state->serveText.c_str(), static_cast<int>(state->serveText.length()));
            SelectObject(hdcMem, hOldFont);
        }

        BitBlt(hdc, 0, 0, rect.right, rect.bottom, hdcMem, 0, 0, SRCCOPY);

        SelectObject(hdcMem, hbmOld);
        DeleteObject(hbmMem);
        DeleteDC(hdcMem);

        EndPaint(hwnd, &ps);
        return 0;
    }
    case WM_TIMER:
    {
        if (wParam == 1 && state)
        {
            HWND robloxHwnd = FindWindowA(NULL, "Roblox");
            if (robloxHwnd)
            {
                RECT rect;
                GetWindowRect(robloxHwnd, &rect);
                int width = rect.right - rect.left;
                int height = rect.bottom - rect.top;

                SetWindowPos(hwnd, HWND_TOPMOST, rect.left, rect.top,
                             width, height, SWP_SHOWWINDOW);

                state->lineX = width / 2;

                switch (state->shm.getInt(ShmVariable::serveMode))
                {
                case 1:
                    state->serveText = "Normal";
                    break;
                case 2:
                    state->serveText = "Advanced";
                    break;
                default:
                    state->serveText = "Skill";
                    break;
                }

                HDC hdc = GetDC(hwnd);
                HFONT hOldFont = (HFONT)SelectObject(hdc, state->gdi.getFont());
                SIZE textSize;
                GetTextExtentPoint32A(hdc, state->serveText.c_str(),
                                      state->serveText.length(), &textSize);
                SelectObject(hdc, hOldFont);
                ReleaseDC(hwnd, hdc);

                state->serveTextX = width - textSize.cx - 10;
                state->serveTextY = height / 2;

                state->textColor = state->shm.getBool(ShmVariable::isServing) ? OverlayConfig::TEXT_ACTIVE_COLOR : OverlayConfig::TEXT_INACTIVE_COLOR;

                state->showLine = state->showText = (GetForegroundWindow() == robloxHwnd);
            }
            else
            {
                state->showLine = state->showText = false;
            }

            InvalidateRect(hwnd, NULL, TRUE);
        }
        return 0;
    }
    case WM_DESTROY:
    {
        KillTimer(hwnd, 1);
        PostQuitMessage(0);
        return 0;
    }
    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    OverlayState state;

    if (!state.shm.initialize())
    {
        MessageBoxA(NULL, "Shared memory initialization failed!", "Error", MB_ICONERROR | MB_OK);
        return 1;
    }

    if (!state.gdi.getFont())
    {
        MessageBoxA(NULL, "Font creation failed!", "Error", MB_ICONERROR | MB_OK);
        return 1;
    }

    WNDCLASSA wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = "OverlayWindowClass";

    if (!RegisterClassA(&wc))
    {
        MessageBoxA(NULL, "Window class registration failed!", "Error", MB_ICONERROR | MB_OK);
        return 1;
    }

    state.overlayHwnd = CreateWindowExA(
        WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
        "OverlayWindowClass",
        OverlayConfig::TITLE.c_str(),
        WS_POPUP,
        OverlayConfig::OFFSET_X, OverlayConfig::OFFSET_Y,
        OverlayConfig::WIDTH, OverlayConfig::HEIGHT,
        NULL, NULL, hInstance, &state);

    if (!state.overlayHwnd)
    {
        MessageBoxA(NULL, "Window creation failed!", "Error", MB_ICONERROR | MB_OK);
        return 1;
    }

    SetLayeredWindowAttributes(state.overlayHwnd, OverlayConfig::BG_COLOR, 0, LWA_COLORKEY);
    ShowWindow(state.overlayHwnd, nCmdShow);

    MSG msg;
    while (GetMessageA(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessageA(&msg);
    }

    return 0;
}