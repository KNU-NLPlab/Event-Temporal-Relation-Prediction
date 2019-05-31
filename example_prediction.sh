
# 입력 format에 맞게 수정 
python maketestdataone.py ..//emb200_full/etTestData/ top_test_all_data.txt

#결과 json파일이 저장될 디렉토리 생성
mkdir link_result_all

# 새로 돌릴때마다 결과 json 디렉토리는 새로 만들거나 기존 저장된 파일들을 모두 지울것
rm link_result_all/*
python predict_json.py  -model models/et_model_20.pt -input top_test_all_data.txt -input_json ../emb200_full/etlink -out_name filename_result.txt -out_json link_result_all/

