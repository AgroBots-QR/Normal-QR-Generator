from fastapi import FastAPI, HTTPException
import qrcode
import os
from starlette.responses import FileResponse

app = FastAPI()
qr_folder = "qrcodes"  # Folder to store QR codes

if not os.path.exists(qr_folder):
    os.makedirs(qr_folder)


def generate_qr_image(latitude: float, longitude: float, location_name: str) -> str:
    location_data = f"geo:{latitude},{longitude}?q={location_name}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(location_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code to a file using the location name
    file_path = os.path.join(qr_folder, f"{location_name}.png")
    img.save(file_path, format='PNG')
    return file_path


@app.post("/generate_qr/")
async def generate_location_qr(latitude: float, longitude: float, location_name: str):
    return generate_qr_image(latitude, longitude, location_name)


@app.get("/download_qr/")
async def download_qr(location_name: str):
    qr_file_path = os.path.join(qr_folder, f"{location_name}.png")

    if not os.path.exists(qr_file_path):
        raise HTTPException(status_code=404, detail="QR code not found")

    return FileResponse(qr_file_path, media_type="image/png", filename=f"{location_name}.png")


@app.get("/qr_info/")
async def qr_info(location_name: str):
    qr_file_path = os.path.join(qr_folder, f"{location_name}.png")

    if not os.path.exists(qr_file_path):
        raise HTTPException(status_code=404, detail="QR code not found")

    return {"location_name": location_name, "qr_path": qr_file_path}
