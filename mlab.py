src = mlab.pipeline.scalar_field(E)
mlab.pipeline.image_plane_widget(src, plane_orientation='x_axes', slice_index=np.abs(x - 1).argmin())
mlab.pipeline.image_plane_widget(src, plane_orientation='y_axes', slice_index=np.abs(y - 1).argmin())
mlab.pipeline.image_plane_widget(src, plane_orientation='z_axes', slice_index=np.abs(z - 1).argmin())
mlab.outline()

mlab.xlabel('tau')
mlab.ylabel('omega')

# mlab.xlabel('omega')
# mlab.ylabel('tau')

mlab.zlabel('p')
mlab.axes(ranges=[x.min(),x.max(),y.min(),y.max(),z.min(),z.max()])
