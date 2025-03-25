<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AeroPath 3D - README</title>
   
</head>
<body>
    <h1>AeroPath 3D</h1>
    <p>AeroPath 3D is a software solution that integrates with the MAVLink mirror stream of Mission Planner. It extracts the geo-location at the center of a tower and generates a precise spiral helical descent path around it. The algorithm triggers the camera at optimal points to capture images for seamless 3D reconstruction of the tower.</p>
    
  <h2>Features</h2>
    <ul>
        <li><strong>Automated Spiral Helical Path:</strong> Generates an optimized descent trajectory for complete tower coverage.</li>
        <li><strong>MAVLink Integration:</strong> Seamlessly connects with Mission Planner’s mirror stream.</li>
        <li><strong>Geo-Referenced Imaging:</strong> Ensures accurate 3D reconstruction using precise geolocation.</li>
        <li><strong>Camera Triggering Algorithm:</strong> Captures high-resolution images at key waypoints.</li>
        <li><strong>Optimized Image Stitching:</strong> Produces a seamless 3D model of the tower.</li>
    </ul>
    
   <h2>Installation</h2>
    <p>Clone the repository:</p>
    <pre><code>git clone https://github.com/your-repo/aeropath3d.git
cd aeropath3d</code></pre>
    <p>Install dependencies:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
    <p>Run the application:</p>
    <pre><code>python app.py</code></pre>
    
  <h2>Field Testing Video</h2>
    <p>Watch our field testing video:</p>
    <a href="https://www.youtube.com/watch?v=YOUR_VIDEO_ID" target="_blank">
        <img src="https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg" alt="AeroPath 3D Field Test">
    </a>
    
  <h2>Usage</h2>
    <ol>
        <li>Launch <strong>AeroPath 3D</strong> and connect to the UAV.</li>
        <li>Select the target tower location.</li>
        <li>Start the mission to generate the helical descent path.</li>
        <li>Monitor real-time image capture and path execution.</li>
        <li>Process the images for 3D reconstruction.</li>
    </ol>
    
</body>
</html>

