# The following has been generated automatically from src/core/raster/qgscontrastenhancement.h
QgsContrastEnhancement.NoEnhancement = QgsContrastEnhancement.ContrastEnhancementAlgorithm.NoEnhancement
QgsContrastEnhancement.StretchToMinimumMaximum = QgsContrastEnhancement.ContrastEnhancementAlgorithm.StretchToMinimumMaximum
QgsContrastEnhancement.StretchAndClipToMinimumMaximum = QgsContrastEnhancement.ContrastEnhancementAlgorithm.StretchAndClipToMinimumMaximum
QgsContrastEnhancement.ClipToMinimumMaximum = QgsContrastEnhancement.ContrastEnhancementAlgorithm.ClipToMinimumMaximum
QgsContrastEnhancement.UserDefinedEnhancement = QgsContrastEnhancement.ContrastEnhancementAlgorithm.UserDefinedEnhancement
try:
    QgsContrastEnhancement.maximumValuePossible = staticmethod(QgsContrastEnhancement.maximumValuePossible)
    QgsContrastEnhancement.minimumValuePossible = staticmethod(QgsContrastEnhancement.minimumValuePossible)
    QgsContrastEnhancement.contrastEnhancementAlgorithmString = staticmethod(QgsContrastEnhancement.contrastEnhancementAlgorithmString)
    QgsContrastEnhancement.contrastEnhancementAlgorithmFromString = staticmethod(QgsContrastEnhancement.contrastEnhancementAlgorithmFromString)
    QgsContrastEnhancement.__group__ = ['raster']
except (NameError, AttributeError):
    pass
