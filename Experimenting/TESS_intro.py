import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory for plots
plot_dir = "plots"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
    print(f"Created directory: {plot_dir}")

def save_plot(filename):
    """Helper function to save plots"""
    filepath = os.path.join(plot_dir, filename)
    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()

#1: Search for TESS data
print("Searching for FFI data...")
search_ffi = lk.search_tesscut('L 98-59')
print("FFI search complete")

print("Searching for target pixel file...")
search_tpf = lk.search_targetpixelfile('L 98-59')
print("TPF search complete")

print("Searching for light curve...")
search_lcf = lk.search_lightcurve('L 98-59')
print("Light curve search complete")

print(search_ffi)
print(search_tpf)
print(search_lcf)

search_lcf_refined = lk.search_lightcurve('L 98-59', author="SPOC", exptime=120)
print(search_lcf_refined)

lcf = search_lcf_refined.download_all()
print(lcf)

#2: create a light curve from the FFI cutout
ffi_data = search_ffi[1].download(cutout_size=10)
plt.figure()
ffi_data.plot()
save_plot("01_ffi_cutout.png")

target_mask = ffi_data.create_threshold_mask(threshold=15, reference_pixel='center')
n_target_pixels = target_mask.sum()
print(f"{n_target_pixels} target pixels found in the FFI cutout.")

plt.figure()
ffi_data.plot(aperture_mask=target_mask, mask_color='r')
save_plot("02_ffi_with_aperture_mask.png")

plt.figure()
ffi_lc = ffi_data.to_lightcurve(aperture_mask=target_mask)
ffi_lc.plot(label="SAP FFI")
save_plot("03_ffi_light_curve.png")

#3: Analize the light curve
plt.figure()
ax = lcf[0].plot(column='pdcsap_flux', normalize=True, label="PDCSAP");
ffi_lc.plot(ax=ax, normalize=True, label="SAP FFI")
save_plot("04_pdcsap_vs_ffi.png")

print("\n" + "="*50)
print("✓ Analysis complete!")
print(f"All plots saved to: {os.path.abspath(plot_dir)}")
print("="*50)