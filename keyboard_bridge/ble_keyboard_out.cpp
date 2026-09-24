#include <BleKeyboard.h>
#include <string.h>

static BleKeyboard bleKeyboard("Amilo-BT", "ESP32-S3", 100);

void bleKeyboardBegin() {
  bleKeyboard.setDelay(0);
  bleKeyboard.begin();
}

bool bleKeyboardConnected() {
  return bleKeyboard.isConnected();
}

void bleKeyboardSend(uint8_t modifiers, const uint8_t keys[6]) {
  KeyReport report;
  report.modifiers = modifiers;
  report.reserved = 0;
  memcpy(report.keys, keys, 6);
  bleKeyboard.sendReport(&report);
}
