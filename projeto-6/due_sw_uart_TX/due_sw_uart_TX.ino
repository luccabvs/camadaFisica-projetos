void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
}

void loop() {
  digitalWrite(8, HIGH);
  _sw_uart_wait_T();

  digitalWrite(8, LOW); 
  _sw_uart_wait_T();

  //caractere

  digitalWrite(8, HIGH); 
  _sw_uart_wait_T();
  
  digitalWrite(8, HIGH); 
  _sw_uart_wait_T();

  digitalWrite(8, LOW); 
  _sw_uart_wait_T();

  digitalWrite(8, LOW); 
  _sw_uart_wait_T();

  digitalWrite(8, LOW); 
  _sw_uart_wait_T();

  digitalWrite(8, LOW); 
  _sw_uart_wait_T();

  digitalWrite(8, HIGH); 
  _sw_uart_wait_T();

  digitalWrite(8, LOW); 
  _sw_uart_wait_T();

  digitalWrite(8, HIGH); 
  _sw_uart_wait_T();

  digitalWrite(8, HIGH); 
  _sw_uart_wait_T();

  delay(2000);
  
}

void _sw_uart_wait_half_T() {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T() {
  _sw_uart_wait_half_T();
  _sw_uart_wait_half_T();
}
