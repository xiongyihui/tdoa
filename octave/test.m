

x1 = 0:1:10;

for i = 1:10
  x2 = [zeros(1, i), x1];

  delay = gcc_phat(x2, x1)
end