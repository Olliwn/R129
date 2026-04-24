cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

project(r129_diag C)

target_sources(app PRIVATE
    src/main.c
    src/ble_diag.c
    src/uart_log.c
    ../payload/r129_payload.c
)

target_include_directories(app PRIVATE src ../payload)
