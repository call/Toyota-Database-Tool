# Toyota-Database-Tool

Hello. This is a program for data mining Toyota cars.
As of Spring 2020, there is no official public database for shopping for Toyota vehicles. Instead, there's only a unique website for each Toyota dealership in the United States. If you were shopping for a new Toyota, wouldn't it be much more efficient to search through all of the Toyota cars at once instead of having to visit each website?

Algorithm:
1. Use https://www.toyota.com/dealers/ to find all of the dealership URLs in the US by entering every valid zipcode in the search bar.
2. Go to every dealership website, find the 'search inventory' link, click it
3. Search through usual inventory of ~200-300 cars by hitting 'next page', and create list of all 'more info about this car' URLs.
4. Go to every car details URL, find the VIN number and price
5. Use secondary VIN lookup tools like https://www.toyota.com/owners/my-vehicle/vehicle-specification to pull the car details from VIN
6. Build .json file

Note: this is not a live database, only a snapshot of Toyota's inventory on April 9, 2020 for proof of concept.
