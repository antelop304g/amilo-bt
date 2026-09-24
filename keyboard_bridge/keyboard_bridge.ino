/*
 * 阿米洛熊猫（或任意标准 USB 键盘）→ 蓝牙键盘
 *
 * 板子：ESP32-S3 SuperMini。Type-C 当 USB 主机接键盘，5V/GND 脚接充电器。
 *
 * Arduino IDE：
 *   开发板包 esp32 by Espressif，要新到示例里能看到 USBHostKeyboard。
 *   ESP32 BLE Keyboard（作者 T-vK）库管理器里搜不到，
 *   从 https://github.com/T-vK/ESP32-BLE-Keyboard 下载 zip，
 *   解压到 ~/Documents/Arduino/libraries/。
 *   开发板：ESP32S3 Dev Module
 *   USB Mode：USB-OTG (TinyUSB)
 *   USB CDC On Boot：Disabled
 *   Flash Size：4MB
 *   PSRAM：Disabled（如果这块板没有 PSRAM）
 *   Partition Scheme：Huge APP（蓝牙加 USB 主机，默认分区放不下）
 *   CPU Frequency：80MHz（蓝牙能用的最低档，240MHz 时板子很烫）
 *
 * 这两项不要同时打开：USB-OTG 和 USB CDC On Boot。
 * 它们共用一个 USB 口，一起开会抢主机。
 *
 * 烧录时 Type-C 插电脑。端口不出现就按住 B，点一下 R，再松开 B。
 * 烧完拔掉电脑，改接充电器和键盘。
 */

#include <USBHost.h>
#include <USBHostHIDKeyboard.h>

USBHostHIDKeyboard usbKeyboard;

extern void bleKeyboardBegin();
extern bool bleKeyboardConnected();
extern void bleKeyboardSend(uint8_t modifiers, const uint8_t keys[6]);

static void onKeyboardReport(uint8_t modifiers, const uint8_t keys[6], void *arg) {
  (void)arg;
  if (!bleKeyboardConnected()) {
    return;
  }
  bleKeyboardSend(modifiers, keys);
}

void setup() {
  bleKeyboardBegin();
  usbKeyboard.setNotifyOnChangeOnly(true);
  usbKeyboard.setReportCallback(onKeyboardReport);
  usbKeyboard.registerWithHost();
  USBHost.begin();
}

void loop() {
  USBHost.task();
  delay(2);
}
