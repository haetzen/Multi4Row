id = 2
x = 4
for i in range(1, x+1):
    if i != id:
        print(i)
        
def update_data(self):
    data = Client.recieve_data(self.client)
    if data != []:
        if data[0] == self.id:
            self.gridpos_x = data[1]
            self.x = self.gridpos_x * self.cellsize + self.offset_grid
            if self.data[2] == 1:
                self.dropping = True
            else:
                self.dropping = False