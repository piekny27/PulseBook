#include <main.h>


//interrups
#define REPORTING_PERIOD_MS 250
#define LOADING_PERIOD_MS 30
#define DONE_PERIOD_MS 50
#define MEASURE_PERIOD_MS 5000
#define NEXT_MEASURE_PERIOD_MS 2000
#define NEXT_POST_PERIOD_MS 2000

const char* serverName = "http://mpkmateusz.pythonanywhere.com/device";
//const char* serverName = "https://192.168.0.105:5000/device";
int configState = 0;

//oled
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64 
#define OLED_RESET -1 
#define SCREEN_ADDRESS 0x3C 

//wifi
const char* ssid[] = {"LenovoZ6 Pro","test","Dom 2.4"};
const char* password[] = {"0","1234567890","bellabella1"};
WiFiClient client;
HTTPClient http;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
PulseOximeter pox;
ESP8266WebServer server(80);
DynamicJsonDocument doc(1024);
String jsonOutput;
DynamicJsonDocument httpRequestData(1024);
String httpRequestDataJSON;

uint32_t tsLastReport = 0;
uint32_t tsLastDone = 0;
uint32_t tsLastPoint = 0;
uint32_t tsLastMeasure = 0;
uint32_t tsNextMeasure = 0;
uint32_t tsNextPOST = 0;
uint8_t sp=0;
uint8_t spArray[20];
float hrArray[20];
float hr=0;
int frame1=0;
int frame2=0;
int measureCount=0;
int wifiCount=0;
bool isWifi=false;
bool isMeasure =false;
bool isDone=false;

String device_key = "5c:cf:7f:94:ed:f7";
String serial_number = "1D5eFq12Y-2022";
String version = "v1.0.0";
String pin = "";
byte configured = false;
bool pinGenerated = false;



void clearMeasurements()
{
  for(int i =0;i<20;i++){
    hrArray[i]=0;
    spArray[i]=0;
  }
}

void drawDone(int x,int y,int width,int height,int frame)
{
	switch (frame)
{
case 0:
  display.fillRect(x,y,width,height,BLACK);
  display.drawBitmap(x, y,bitMapdone1,width,height, 1);
  display.display();
  break;

case 1:
display.fillRect(x,y,width,height,BLACK);
  display.drawBitmap(x, y,bitMapdone2,width,height, 1);
  display.display();
  break;

case 2:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone3,width,height, 1);
display.display();
break;

case 3:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone4,width,height, 1);
display.display();
break;

case 4:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone5,width,height, 1);
display.display();
break;

case 5:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone6,width,height, 1);
display.display();
break;

case 6:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone7,width,height, 1);
display.display();
break;

case 7:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone8,width,height, 1);
display.display();
break;

case 8:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone9,width,height, 1);
display.display();
break;

case 9:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone10,width,height, 1);
display.display();
break;

case 10:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,bitMapdone11,width,height, 1);
display.display();
break;
}
}

void drawLoading(int x, int y, int width, int height, int frame) {
  
switch (frame)
{
case 0:
  display.fillRect(x,y,width,height,BLACK);
  display.drawBitmap(x, y,myBitmapframe_00_delay_0,width,height, 1);
  display.display();
  break;

case 1:
display.fillRect(x,y,width,height,BLACK);
  display.drawBitmap(x, y,myBitmapframe_01_delay_0,width,height, 1);
  display.display();
  break;

case 2:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_02_delay_0,width,height, 1);
display.display();
break;

case 3:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_03_delay_0,width,height, 1);
display.display();
break;

case 4:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_04_delay_0,width,height, 1);
display.display();
break;

case 5:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_05_delay_0,width,height, 1);
display.display();
break;

case 6:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_06_delay_0,width,height, 1);
display.display();
break;

case 7:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_07_delay_0,width,height, 1);
display.display();
break;

case 8:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_08_delay_0,width,height, 1);
display.display();
break;

case 9:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_09_delay_0,width,height, 1);
display.display();
break;

case 10:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_10_delay_0,width,height, 1);
display.display();
break;

case 11:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_11_delay_0,width,height, 1);
display.display();
break;

case 12:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_12_delay_0,width,height, 1);
display.display();
break;

case 13:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_13_delay_0,width,height, 1);
display.display();
break;

case 14:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_14_delay_0,width,height, 1);
display.display();
break;

case 15:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_15_delay_0,width,height, 1);
display.display();
break;

case 16:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_16_delay_0,width,height, 1);
display.display();
break;

case 17:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_17_delay_0,width,height, 1);
display.display();
break;

case 18:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_18_delay_0,width,height, 1);
display.display();
break;

case 19:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_19_delay_0,width,height, 1);
display.display();
break;

case 20:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_20_delay_0,width,height, 1);
display.display();
break;

case 21:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_21_delay_0,width,height, 1);
display.display();
break;

case 22:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_22_delay_0,width,height, 1);
display.display();
break;

case 23:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_23_delay_0,width,height, 1);
display.display();
break;

case 24:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_24_delay_0,width,height, 1);
display.display();
break;

case 25:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_25_delay_0,width,height, 1);
display.display();
break;

case 26:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_26_delay_0,width,height, 1);
display.display();
break;

case 27:
display.fillRect(x,y,width,height,BLACK);
display.drawBitmap(x, y,myBitmapframe_27_delay_0,width,height, 1);
display.display();
break;
}
}

void displayOximeterPrint(float heartRate, uint8_t spO2) 
{
  display.setTextSize(2);     

  String hr = "";
  String sp = "";
  hr.concat(heartRate);
  sp.concat(spO2);

  display.fillRect(0,0,110,64,BLACK);
  display.setCursor(0, 0);
  display.write("Heart rate");
  display.setCursor(0, 18);
  display.write(hr.c_str());
  display.write("bpm");
  display.setCursor(0, 36);
  display.write("SpO2:");
  display.write(sp.c_str());
  display.write("%");

  display.display();
}

void wifiScan(bool autoConnect)
{
	int n = WiFi.scanNetworks();
	int y=17;

	display.clearDisplay();
	display.setTextSize(2);
	display.setCursor(0,0);
	display.write("WiFi:");
	display.print(n);
	display.setTextSize(1);
	display.setCursor(10,y);

	for(int i =0; i<n; i++)
	{
		display.print(WiFi.SSID(i).substring(0,19));
		y+=8;
		display.setCursor(10,y);
	}

	if(autoConnect && !isWifi)
	{
		for(int i =0; i<n; i++)
		{
			if(isWifi) break;
			for(int j=0; j<3; j++)
			{
				if(isWifi) break;
				if(!strcmp(WiFi.SSID(i).c_str(),ssid[j]))
				{

					if(!strcmp("0",password[j]))
					{
						WiFi.begin(ssid[j],"");
						isWifi=true;
					}
					else
					{
						WiFi.begin(ssid[j],password[j]);
						isWifi=true;
					}
				}
			}
		}
	}

	display.display();

}

void wifiRestart(){
 Serial.println("Turning WiFi off...");
 WiFi.mode(WIFI_OFF);
 Serial.println("Trying to connect to WiFi...");
 WiFi.mode(WIFI_STA);
 isWifi=false;
 wifiScan(true);
}

void wifiShow()
{
	while (WiFi.status() != WL_CONNECTED) 
	{
		if((millis() - tsLastPoint > LOADING_PERIOD_MS))
		{
			drawLoading(SCREEN_WIDTH-17,0,17,17,frame1);
			frame1++;
      		if(frame1>27)
			{
				wifiCount++;
				frame1=0;
			} 
			if(wifiCount>=10)
			{
				wifiCount=0;
				wifiRestart();
			} 
			tsLastPoint = millis();
		}
 	}
	display.clearDisplay();
	display.setTextSize(2);
	display.setCursor(0,0);
	display.write("Connected");
	display.setTextSize(1);
	display.setCursor(0,18);
	display.write("SSID: ");
	display.write(WiFi.SSID().c_str());
	display.setCursor(0,26);
	display.write("IP: ");
	display.write(WiFi.localIP().toString().c_str());
	display.display();
	delay(500);
	display.clearDisplay();
}

void poxRestart()
{
	if (!pox.begin()) {
		Serial.println("Pulse oximeter allocation failed");
		for(;;);
	}
	pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
}

void requestIndex()
{
	server.send(200, "text/html", INDEX_HTML);
}

void requestJson()
{
	server.send(200, "text/plain", jsonOutput);
}

int genPin()
{
	return random(1000,9999);
}

void displayFormConfig(String msg)
{
	display.clearDisplay();
	display.setTextSize(2);
	display.setCursor(0,0);
	display.write("Config:");
	display.setTextSize(1);
	display.setCursor(0,18);
	display.write(msg.c_str());
	display.display();
}

void httpPOST()
{
	http.begin(client, serverName);
	http.addHeader("Content-Type", "application/json; charset=utf-8");
	httpRequestData["device_key"]=device_key;
	httpRequestData["serial_number"]=serial_number;
	httpRequestData["version"]=version;
	httpRequestDataJSON = "";
	serializeJson(httpRequestData,httpRequestDataJSON);
	int httpResponseCode = http.POST(httpRequestDataJSON);
	if(httpResponseCode == 205)
	{
		configState = 0;
		configured = false;
		EEPROM.write(0, configured);
		EEPROM.write(1, configState);
		if (EEPROM.commit()) Serial.println("EEPROM successfully reset");
		else Serial.println("ERROR! EEPROM commit failed");
	}	
	http.end();
}


void setup() 
{
	//uart
	Serial.begin(115200);
	
	//eeprom
	EEPROM.begin(512);
	configured = EEPROM.read(0);
	configState = EEPROM.read(1);
	if(configState > 3 || configState < 0)
	{
		configState = 0;
		configured = false;
		EEPROM.write(0, configured);
		EEPROM.write(1, configState);
		if (EEPROM.commit()) Serial.println("EEPROM successfully reset");
		else Serial.println("ERROR! EEPROM commit failed");
	} 

	//oled 128x64
	if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
		Serial.println("Display allocation failed");
		for(;;); 
	}
	display.clearDisplay();
	display.setTextColor(WHITE);
  	display.cp437(true);
	display.drawBitmap((SCREEN_WIDTH/2)-30,(SCREEN_HEIGHT/2)-30,bmp_logo,63,60,1);
	display.display();
	delay(1000);
	display.clearDisplay();

	//wifi
	//client.setInsecure();
	//client.connect(serverName, 443);
	wifiScan(true);
	wifiShow();

	//serwer
	server.on("/", requestIndex);
	server.on("/json", requestJson);
  	server.begin();

	poxRestart();

}

void loop() {

  server.handleClient();

  if(configState<=2 && !configured)
  {
	if((millis() - tsNextPOST) > NEXT_POST_PERIOD_MS)
	  {
		if(WiFi.status()== WL_CONNECTED)
		{
			http.begin(client, serverName);
			http.addHeader("Content-Type", "application/json; charset=utf-8");
			
			if(configState == 0)
			{	
				httpRequestData["device_key"]=device_key;
				httpRequestData["serial_number"]=serial_number;
				httpRequestData["version"]=version;
				httpRequestDataJSON = "";
				serializeJson(httpRequestData,httpRequestDataJSON);
				int httpResponseCode = http.POST(httpRequestDataJSON);
				displayFormConfig("Step 1-Paste your D/K");
				if(httpResponseCode == 202) //202-accepted
				{
					displayFormConfig("Step 1-D/K correct");
					configState++;
				}	
				if(httpResponseCode == 205)
				{
					configState=0;
				}	
			}
			else if (configState == 1)
			{
				if(!pinGenerated)
				{
					pin = genPin();
					pinGenerated = true;
				} 
				httpRequestData["device_key"]=device_key;
				httpRequestData["serial_number"]=serial_number;
				httpRequestData["version"]=version;
				httpRequestData["pin"]=pin;
				httpRequestDataJSON = "";
				serializeJson(httpRequestData,httpRequestDataJSON);
				int httpResponseCode = http.POST(httpRequestDataJSON);
				String scr = "Step 2-PIN:" + pin;
				displayFormConfig(scr);		

				if(httpResponseCode == 202) //202-accepted
				{
					displayFormConfig("Step 2-Correct PIN!");
					pinGenerated = false;
					configState++;
				}
				if(httpResponseCode == 205)
				{
					configState=0;
				}
			}
			else if (configState == 2)
			{
				Serial.print("finish/device_key");
				Serial.println(configState);
				displayFormConfig("Step 3-Config done");
				poxRestart();
				configState++;
				configured = true;
				EEPROM.write(0, configured);
				EEPROM.write(1, configState);
				if (EEPROM.commit()) Serial.println("EEPROM successfully committed");
				else Serial.println("ERROR! EEPROM commit failed");
			}			
			http.end();
		}
	  tsNextPOST = millis();
    }
  }
  else
  {
	pox.update();

	if (millis() - tsLastReport > REPORTING_PERIOD_MS) 
	{
		hr=pox.getHeartRate();
		sp=pox.getSpO2();
		displayOximeterPrint(hr,sp);
		if(hr>0 && sp>0 && sp<=100)
		{
		if(!isMeasure)
		{
			tsLastMeasure = millis();
		}
		isMeasure=true;
		hrArray[measureCount] = hr;
		spArray[measureCount]= sp;
		measureCount++;
		if(measureCount>19) measureCount=0;
		if ((millis() - tsLastMeasure > MEASURE_PERIOD_MS) && isMeasure) 
		{
			for(int i=0; i<20;i++)
			{
				httpRequestData["hr_array[]"][i] = hrArray[i]; 
				httpRequestData["sp_array[]"][i] = spArray[i];
			}
			httpPOST();
			tsLastMeasure = millis();
			clearMeasurements();
			poxRestart();
			isMeasure=false;
			isDone=true;
		}
		
		} 
		else
		{
		if(isMeasure) clearMeasurements();
		drawLoading(SCREEN_WIDTH-18,SCREEN_HEIGHT-18,17,17,15);
		measureCount=0;
		isMeasure=false;
		isDone=false;
		frame2=0;
		}
		tsLastReport = millis();
	}

	if((millis() - tsLastPoint > LOADING_PERIOD_MS) && hr>0 && sp>0 && sp<=100)
	{
		if(isDone)
		{
			if((millis() - tsLastDone > DONE_PERIOD_MS))
			{
				drawDone(SCREEN_WIDTH-18,SCREEN_HEIGHT-18,17,17,frame2);
				frame2++;
				if(frame2>10) frame2=10;
				tsLastDone = millis();
			}
			tsLastPoint = millis();
		}
		else
		{
		drawLoading(SCREEN_WIDTH-18,SCREEN_HEIGHT-18,17,17,frame1);
		frame1++;
		if(frame1>27) frame1=0;
		tsLastPoint = millis();
		}
	}
  }

  if(WiFi.status() != WL_CONNECTED)
  {
	wifiScan(true);
	wifiShow();
	poxRestart();
  }
}


