from model.model import predict
import warnings

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    print(predict(['30', '1', '2020', '3.0', '350', '1694', '844', '1189', '12', '352'], 'data', 'car_model'))
