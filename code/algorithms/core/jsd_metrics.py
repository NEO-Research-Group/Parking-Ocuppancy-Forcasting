from sklearn import metrics
import json


def report_metrics(y_true, y_pred, folder_name, exp_name):
  
  metrics_json = {}
  metrics_json["explained_variance"] = metrics.explained_variance_score(y_true, y_pred)
  metrics_json["mean_absolute_error"] = metrics.mean_absolute_error(y_true, y_pred)
  metrics_json["mean_squared_error"] = metrics.mean_squared_error(y_true, y_pred)  
  metrics_json["root_mean_squared_error"] = metrics.mean_squared_error(y_true, y_pred, squared=False)    
  
  #metrics_str = "Explained Variance:\n\t" + str(metrics.explained_variance_score(y_true, y_pred))
  #metrics_str = metrics_str + "MAE:\n\t" + str(metrics.mean_absolute_error(y_true, y_pred)) 
  metrics_str = json.dumps(metrics_json)
  text_file = open("../../results/" + folder_name + '/metrics_' + exp_name + '.txt', "w")
  n = text_file.write(metrics_str)
  text_file.close()
  return metrics_str
