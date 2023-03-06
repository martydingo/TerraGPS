# TerraGPS

## Overview 

A simple class to get the position of a player in Terraria via the Terraria API and paint it onto the world image, by polling the API of a tShock-enabled Terraria server and painting onto a pre-generated world image (such as one created by [TerraMapper](https://github.com/martydingo/TerraMapper)).

## Usage

Call the `TerraGPS` class, providing the required parameters, e.g.

```python
from TerraGPS import TerraGPS

tshock_token = "<REDACTED>"
tshock_host = "1.2.3.4"
input_image = "Cool_World_Name.png"
output_image = "Cool_World_Name_Cartographer.png"

tGPS = TerraGPS(
    tshock_host=tshock_host,
    tshock_token=tshock_token,
    input_image=input_image,
    output_image=output_image,
)
```