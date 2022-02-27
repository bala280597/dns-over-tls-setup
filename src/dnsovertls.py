import socket
import ssl
import sys

def send_query(tsock,dns_query):
  # Send and Receive data
  tsock.send(dns_query)
  result=tsock.recv(1024)
  tsock.close()
  return result

def tls_connection(dns,port):
  # TLS Wrapping 
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(10)
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=dns)
  wrappedSocket.connect((dns , int(port)))
  return wrappedSocket

# send new request to upstream dns server and return the result
def new_request(data,address,dns,port):
  tsock=tls_connection(dns,port)
  tcp_result = send_query(tsock, data)
  if tcp_result:
    # Get first 6 bytes from response
    rcode = tcp_result[:6].encode("hex")
    # Get 12th bit from the response
    rcode = str(rcode)[11:]
    # Check 12 th bit with condition
    if (rcode != '0'):
      sys.exit('Error RCODE', rcode)
    else:
      return tcp_result
  else:
    sys.exit('Error occurred')

if __name__ == '__main__':
  HEADER = 1024
  # Proxy server and Port
  port = 12555
  host='0.0.0.0'
  # DNS server and Port
  dns_server = '1.1.1.1'
  dns_port   = 853
  ADDR = (host, port)
  try:
    # Socket Connection and Binding
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen(10)
    while True:
      # Receive DNS query from client
      conn, addr = s.accept()
      data = conn.recv(HEADER)
      result = new_request(data, addr, dns_server, dns_port)
      conn.sendto(result, addr)
  except:
    s.close()
