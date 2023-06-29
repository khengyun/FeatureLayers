from featurelayers.models.LBC_xception import LBC_Xception




model = LBC_Xception(include_top=True,input_shape=(128,128,3),weights=None,classes=1000)
model.summary()