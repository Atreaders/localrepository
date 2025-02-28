import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def ring_resonator_structure():
    # Define materials (assuming silicon on silica)
    n_silicon = 3.45  # Silicon refractive index
    n_silica = 1.44   # Silica refractive index
    
    # Define the waveguide and ring dimensions
    wg_width = 0.5  # Waveguide width
    wg_thickness = 0.5 # Waveguide thickness
    ring_radius = 3.0  # Ring radius
    ring_width = 0.5  # Ring width
    ring_thickness = 0.5  # Ring thickness (now used in visualization)
    gap = 0.2  # Gap between ring and waveguides (updated value)
    
    # Define geometric objects
    waveguides = [
        {"type": "block", 
        "size": (10, wg_width, wg_thickness), 
        "center": (0, ring_radius + gap, 0), 
        "material": "silicon"},
        {"type": "block", 
         "size": (10, wg_width, wg_thickness), 
         "center": (0, -ring_radius - gap, 0), 
         "material": "silicon"}
    ]
    
    ring = {"type": "torus", 
            "radius": ring_radius, 
            "thickness": ring_width, 
            "height": ring_thickness, 
            "material": "silicon"}
    
    geometry = waveguides + [ring]
    
    return geometry

def plot_structure(geometry):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-1, 1)
    ax.set_xlabel("X-axis (μm)")
    ax.set_ylabel("Y-axis (μm)")
    ax.set_zlabel("Z-axis (μm)")
    
    # Draw waveguides
    for obj in geometry:
        if obj["type"] == "block":
            x, y, z = obj["center"]
            width, height, thickness = obj["size"]
            vertices = [
                [x - width/2, y - height/2, z - thickness/2],
                [x + width/2, y - height/2, z - thickness/2],
                [x + width/2, y + height/2, z - thickness/2],
                [x - width/2, y + height/2, z - thickness/2],
                [x - width/2, y - height/2, z + thickness/2],
                [x + width/2, y - height/2, z + thickness/2],
                [x + width/2, y + height/2, z + thickness/2],
                [x - width/2, y + height/2, z + thickness/2]
            ]
            faces = [[vertices[j] for j in [0, 1, 2, 3]], [vertices[j] for j in [4, 5, 6, 7]],
                     [vertices[j] for j in [0, 1, 5, 4]], [vertices[j] for j in [2, 3, 7, 6]],
                     [vertices[j] for j in [0, 3, 7, 4]], [vertices[j] for j in [1, 2, 6, 5]]]
            ax.add_collection3d(Poly3DCollection(faces, color='gray', alpha=0.7))
    
    # Draw ring resonator as a torus with height
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 50)
    theta, phi = np.meshgrid(theta, phi)
    r, w, h = geometry[-1]["radius"], geometry[-1]["thickness"] / 2, geometry[-1]["height"] / 2
    
    X = (r + w * np.cos(phi)) * np.cos(theta)
    Y = (r + w * np.cos(phi)) * np.sin(theta)
    Z = h * np.sin(phi)
    ax.plot_surface(X, Y, Z, color='blue', alpha=0.6)
    
    plt.title("3D Ring Resonator Structure")
    plt.show()
    
structure = ring_resonator_structure()
print("Ring resonator structure defined:", structure)
plot_structure(structure)
    