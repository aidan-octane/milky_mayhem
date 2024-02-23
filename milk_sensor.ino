#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>

const char *ssid = "";
const char *password = "";
const char *serverIP = "";
const int serverPort = 50005;  // Flask server port
const String endpoint = "/add_data";

const int io_pin = 5;
bool milk = true;

int currentValue, previousValue;

void setup() {
  // Initialize serial monitor
  Serial.begin(115200);
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  Serial.println("Initialized");
  // Connects to WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
  // Initializes and equalizes the sensor
  pinMode(io_pin, INPUT);
  Serial.println("Delaying for 30 seconds...");
  delay(30000);
  Serial.println("Beginning milk checking");
}

void loop() {
  // Runs loop program for about 6.5 hours, then restarts
  for (int i = 0; i < 100000; i++) {
    delay(250);
    currentValue = digitalRead(io_pin);
    Serial.println(currentValue);
    if (currentValue == 1) {
      Serial.println("Milk gone!");
      triggerMilkGone();
      milk = false;
      // waits for milk to return :D
      while (digitalRead(io_pin) != 0) {
        delay(1000);
      }
    }
  }
  ESP.restart();
}

void triggerMilkGone() {
  // Create an HTTP client object
  HTTPClient http;

  // Specify the server and port
  http.begin(serverIP, serverPort, endpoint);

  // Set content type and payload for POST request
  http.addHeader("Content-Type", "application/json");

  // Get the current time as Unix timestamp
  time_t timestamp = time(nullptr);
  // Create JSON payload
  String jsonPayload = "{\"value\": 1, \"timestamp\": " + String(timestamp) + "}";

  // Send POST request
  int httpResponseCode = http.POST(jsonPayload);

  // Check the response code
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // Print the response payload
    String payload = http.getString();
    Serial.println("Response payload: " + payload);
  } else {
    Serial.print("HTTP Request failed. Error code: ");
    Serial.println(httpResponseCode);
  }

  // Close connection
  http.end();

  // Wait for some time before making the next request
  Serial.println("Delaying...");
   delay(10000);
}
