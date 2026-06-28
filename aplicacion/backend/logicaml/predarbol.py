
import pandas as pd
import pickle

class ModeloInversor:
    def __init__(self, ruta_modelo="D:\\DocumentosI\\EDUCATIVA+\\4to Semestre\\ProyectoNeoNet\\EntrenamientoBosque\\modelo_xgboost.pickle"):
        with open(ruta_modelo, "rb") as f:
            datos_cargados = pickle.load(f)
  
        if isinstance(datos_cargados, dict):
      
            if "modelo" in datos_cargados:
                self.modelo = datos_cargados["modelo"]
            elif "model" in datos_cargados:
                self.modelo = datos_cargados["model"]
            else:
                primera_llave = list(datos_cargados.keys())[0]
                self.modelo = datos_cargados[primera_llave]
        else:

            self.modelo = datos_cargados
        
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
        
        prediccion = self.modelo.predict(df_final)[0]
        return self.perfiles.get(prediccion, "Desconocido")