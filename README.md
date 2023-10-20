# Fetch Backend Take Home Exercise

### Prerequisites

- Docker

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone git@github.com:JackalQiX/Fetch-backend.git

2. Change to the project directory:
   
   ```bash
   cd fetch-backend

3. Load the docker image:
   
   ```bash
   docker load < fetch-backend.tar

4. Run the image:
   
   ```bash
   docker run -it -p 5000:5000 -d fetch-backend
   
This will start the server, and you can access the application at http://localhost:5000.

### APIs

/receipts/process (POST): Process receipt data, calculate points, and return a receipt ID.

/receipts/{id}/points (GET): Retrieve the number of points awarded for a specific receipt by its ID.

Detailed documentation for each endpoint can be found in the code comments.
