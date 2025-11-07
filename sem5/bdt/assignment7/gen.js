import fs from 'fs'

const locations = ['Pune', 'Mumbai', 'Delhi', 'Hyderabad', 'Bangalore']

const file = await fs.promises.readFile('./Mall_Customers.csv', {encoding:'utf8'})

console.log('CustomerID,Location')
for (const line of file.trim().split('\r\n').slice(1)) {
  console.log(line.split(',')[0] + ',' + locations[Math.floor(Math.random()*locations.length)])
}
