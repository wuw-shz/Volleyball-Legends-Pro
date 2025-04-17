#pragma once
#include <windows.h>
#include <string>

enum class ShmVariable {
    isInServeLoop,
    isServing,
    isServe,
    isToss,
    serveCommand,
    serveMode,
    COUNT
};

class SharedMemory {
public:
    SharedMemory();
    ~SharedMemory();

    bool initialize();
    void setBool(ShmVariable var, bool value);
    bool getBool(ShmVariable var) const;
    void setInt(ShmVariable var, int value);
    int getInt(ShmVariable var) const;
    bool isInitialized() const { return m_initialized; }

private:
    static constexpr size_t SLOT_SIZE = 4;
    static constexpr size_t BUFFER_SIZE = SLOT_SIZE * static_cast<size_t>(ShmVariable::COUNT);
    static constexpr LPCWSTR SHARED_MEM_NAME = L"VolleyballLegendsProSharedMemory";

    HANDLE m_mapFile = nullptr;
    unsigned char* m_buffer = nullptr;
    bool m_initialized = false;

    void cleanup();
};