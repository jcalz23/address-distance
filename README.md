# Address Distance Calculator

A web application that calculates the driving distance between pairs of addresses from a CSV file using Google Maps API.

## Setup Instructions

### Prerequisites
1. Install Miniconda or Anaconda from https://docs.conda.io/en/latest/miniconda.html
2. Get a Google Maps API key from https://console.cloud.google.com/
   - Enable the "Distance Matrix API" service
   - Create credentials (API key)
   - Keep this key handy for the setup

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd address-distance

# Create and activate a new conda environment
conda create -n address-distance python=3.9
conda activate address-distance

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Create .env file in the project root
echo "API_KEY=your_google_maps_api_key_here" > .env
```

### Running the Application
1. Start the backend server (in one terminal):
```bash
# Make sure you're in the project root and conda environment is activated
conda activate address-distance
uvicorn backend.app.main:app --reload --port 8001
```

2. Start the frontend server (in another terminal):
```bash
# Make sure you're in the project root
cd frontend
npm start
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8001/docs

### Using the Application
1. Prepare a CSV file with these columns:
   ```csv
   address1,address2
   "123 Main St, City, State","456 Oak Ave, City, State"
   ```
2. Upload the file using the web interface
3. Wait for processing
4. Download the processed file with distances

### Troubleshooting
- If you see "API key not found" errors, check your .env file
- If the backend won't start, ensure port 8001 is free
- If the frontend won't connect, check that both servers are running
- For CORS issues, ensure you're using the correct ports

## Project Overview

This application allows users to:
1. Upload a CSV file containing pairs of addresses
2. Process the file using Google Maps API to calculate driving distances
3. Download a CSV file with the original data plus distance information

## Simplified Technology Stack

### Backend
- **FastAPI**: Python-based web framework for building APIs
- **Python 3.9+**: Core programming language
- **Google Maps API**: For distance calculations
- **Pandas**: For CSV data manipulation

### Frontend
- **React**: Simple UI with minimal dependencies
- **Plain CSS**: Basic styling without frameworks

### Deployment
- **Vercel**: For simplified cloud deployment

## Implementation Plan

### 1. Backend Development
- [x] Set up Google Maps API key
- [x] Create FastAPI application structure
- [x] Implement file upload endpoint
- [x] Create CSV processing service
- [x] Add file download endpoint
- [x] Add error handling

### 2. Frontend Development
- [x] Create minimal React application
- [x] Build file upload component
- [x] Add download button for processed file
- [x] Implement error display

### 3. Deployment
- [ ] Configure Vercel for deployment
- [ ] Set up environment variables
- [ ] Deploy and test application

## Vercel Deployment Instructions

### Backend Deployment
1. Install Vercel CLI: `npm install -g vercel`
2. In your project directory, run: `vercel`
3. Follow the prompts to link to your Vercel account
4. Set environment variables:
   ```
   vercel env add API_KEY
   ```
5. Configure `vercel.json` in your project root:
   ```json
   {
     "version": 2,
     "builds": [
       { "src": "backend/app/main.py", "use": "@vercel/python" }
     ],
     "routes": [
       { "src": "/api/(.*)", "dest": "backend/app/main.py" }
     ],
     "env": {
       "API_KEY": "@api_key"
     }
   }
   ```
6. Deploy: `vercel --prod`

### Frontend Deployment
Frontend can be deployed separately using:
1. Build your React app: `npm run build`
2. Deploy the build folder: `vercel --prod`

Alternatively, use Vercel's GitHub integration for automatic deployments.

## CSV Format Requirements
- Input CSV must have columns: `address1`, `address2`
- Output CSV will have columns: `address1`, `address2`, `distance_miles`

## Project Structure
```
address-distance/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helper functions
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   └── App.js           # Main application
│   ├── package.json        # JS dependencies
└── vercel.json            # Vercel configuration
```

## Next Steps
1. Initialize the FastAPI project
2. Create a simple React frontend
3. Implement CSV processing functionality
4. Deploy to Vercel
