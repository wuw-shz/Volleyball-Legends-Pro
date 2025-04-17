#include "SharedMemory.h"
#include <stdexcept>
#include <iostream>

SharedMemory::SharedMemory() = default;

SharedMemory::~SharedMemory() {
    cleanup();
}

bool SharedMemory::initialize() {
    if (m_initialized) {
        return true;
    }

    SECURITY_ATTRIBUTES sa = { sizeof(SECURITY_ATTRIBUTES), nullptr, FALSE };
    SECURITY_DESCRIPTOR sd{};
    InitializeSecurityDescriptor(&sd, SECURITY_DESCRIPTOR_REVISION);
    SetSecurityDescriptorDacl(&sd, TRUE, nullptr, FALSE);
    sa.lpSecurityDescriptor = &sd;

    m_mapFile = CreateFileMappingW(
        INVALID_HANDLE_VALUE,
        &sa,
        PAGE_READWRITE,
        0,
        BUFFER_SIZE,
        SHARED_MEM_NAME
    );

    if (m_mapFile == nullptr) {
        std::cerr << "Couldnt create file mapping object: " << GetLastError() << std::endl;
        return false;
    }

    m_buffer = static_cast<unsigned char*>(MapViewOfFile(
        m_mapFile,
        FILE_MAP_ALL_ACCESS,
        0, 0, BUFFER_SIZE
    ));

    if (m_buffer == nullptr) {
        std::cerr << "Could not map view of file: " << GetLastError() << std::endl;
        CloseHandle(m_mapFile);
        m_mapFile = nullptr;
        return false;
    }

    /*for (size_t i = 0; i < BUFFER_SIZE; ++i) {
        m_buffer[i] = 0;
    }*/

    m_initialized = true;
    return true;
}

void SharedMemory::cleanup() {
    if (m_buffer) {
        UnmapViewOfFile(m_buffer);
        m_buffer = nullptr;
    }
    if (m_mapFile) {
        CloseHandle(m_mapFile);
        m_mapFile = nullptr;
    }
    m_initialized = false;
}

void SharedMemory::setBool(ShmVariable var, bool value) {
    if (!m_initialized || !m_buffer) {
        throw std::runtime_error("Shared memory not initialized");
    }

    size_t index = static_cast<size_t>(var);
    if (index >= static_cast<size_t>(ShmVariable::COUNT)) {
        throw std::out_of_range("Variable index out of range");
    }

    m_buffer[index * SLOT_SIZE] = value ? 1 : 0;
}

bool SharedMemory::getBool(ShmVariable var) const {
    if (!m_initialized || !m_buffer) {
        std::cerr << "Shared memory not initialized" << std::endl;
        return false;
    }

    size_t index = static_cast<size_t>(var);
    if (index >= static_cast<size_t>(ShmVariable::COUNT)) {
        std::cerr << "Variable index out of range" << std::endl;
        return false;
    }

    return m_buffer[index * SLOT_SIZE] != 0;
}

void SharedMemory::setInt(ShmVariable var, int value) {
    if (!m_initialized || !m_buffer) {
        throw std::runtime_error("Shared memory not initialized");
    }

    size_t index = static_cast<size_t>(var);
    if (index >= static_cast<size_t>(ShmVariable::COUNT)) {
        throw std::out_of_range("Variable index out of range");
    }

    *reinterpret_cast<int*>(&m_buffer[index * SLOT_SIZE]) = value;
}

int SharedMemory::getInt(ShmVariable var) const {
    if (!m_initialized || !m_buffer) {
        std::cerr << "Shared memory not initialized" << std::endl;
        return 0;
    }

    size_t index = static_cast<size_t>(var);
    if (index >= static_cast<size_t>(ShmVariable::COUNT)) {
        std::cerr << "Variable index out of range" << std::endl;
        return 0;
    }

    return *reinterpret_cast<int*>(&m_buffer[index * SLOT_SIZE]);
}