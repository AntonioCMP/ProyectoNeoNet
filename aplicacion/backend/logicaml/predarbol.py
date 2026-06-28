
import pandas as pd
import pickle

class ModeloInversor:
    def __init__(self, ruta_modelo="D:\\DocumentosI\\EDUCATIVA+\\4to Semestre\\ProyectoNeoNet\\EntrenamientoBosque\\modelo_xgboost.pickle"):
        with open(ruta_modelo, "rb") as f:
            self.modelo = pickle.load(f)
        
        self.columnas_esperadas = [
            'age', 'gender_Male', 'Factor_Returns', 'Factor_Risk',
            'Objective_Growth', 'Objective_Income', 'Purpose_Savings for Future', 
            'Purpose_Wealth Creation', 'Duration_3-5 years', 'Duration_Less than 1 year', 
            'Duration_More than 5 years', 'Expect_20%-30%', 'Expect_30%-40%'
        ]
        self.perfiles = {0: "Arriesgado", 1: "Conservador", 2: "Moderado"}

    def predecir_perfil(self, datos_dict):
        df_usuario = pd.DataFrame([datos_dict])
        df_dummies = pd.get_dummies(df_usuario)
        df_final = df_dummies.reindex(columns=self.columnas_esperadas, fill_value=0)
        
        prediccion = self.modelo.pred(df_final)[0]
        return self.perfiles.get(prediccion, "Desconocido")