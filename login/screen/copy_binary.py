with open('pic.jpg', 'rb') as f:
  m=f.read()


with open('received.jpg', 'wb') as q:
  q.write(m)

