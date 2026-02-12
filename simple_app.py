from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from simple_predictor import SimplePredictor

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='template')

# Initialize predictor
try:
    predictor = SimplePredictor()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    predictor = None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("vehicledata.html", {"request": request, "context": None})

@app.post("/", response_class=HTMLResponse)
async def predict(request: Request,
                 Gender: int = Form(...),
                 Age: int = Form(...),
                 Driving_License: int = Form(...),
                 Region_Code: float = Form(...),
                 Previously_Insured: int = Form(...),
                 Annual_Premium: float = Form(...),
                 Policy_Sales_Channel: float = Form(...),
                 Vintage: int = Form(...),
                 Vehicle_Age_lt_1_Year: int = Form(...),
                 Vehicle_Age_gt_2_Years: int = Form(...),
                 Vehicle_Damage_Yes: int = Form(...)):
    
    try:
        if predictor is None:
            return templates.TemplateResponse("vehicledata.html", 
                {"request": request, "context": "Model not loaded"})
        
        # Prepare data
        data = {
            "Gender": [Gender],
            "Age": [Age],
            "Driving_License": [Driving_License],
            "Region_Code": [Region_Code],
            "Previously_Insured": [Previously_Insured],
            "Annual_Premium": [Annual_Premium],
            "Policy_Sales_Channel": [Policy_Sales_Channel],
            "Vintage": [Vintage],
            "Vehicle_Age_lt_1_Year": [Vehicle_Age_lt_1_Year],
            "Vehicle_Age_gt_2_Years": [Vehicle_Age_gt_2_Years],
            "Vehicle_Damage_Yes": [Vehicle_Damage_Yes]
        }
        
        # Make prediction
        prediction = predictor.predict(data)
        result = "Response-Yes" if prediction[0] == 1 else "Response-No"
        
        return templates.TemplateResponse("vehicledata.html", 
            {"request": request, "context": result})
        
    except Exception as e:
        return templates.TemplateResponse("vehicledata.html", 
            {"request": request, "context": f"Error: {str(e)}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_app:app", host="127.0.0.1", port=4000, reload=True)