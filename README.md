<H3> 한국어 사건 단어-시간 표현 관계 추정 모델 </H3>  

---
  

![model](https://user-images.githubusercontent.com/37574306/58693490-debc6880-83cb-11e9-8ed6-2abbddd19655.png)

주어진 문장과 문장 내 사건 단어와 시간 표현 간의 관계 유무 추정 모델 코드  
관계 추정은 둘의 관계가 있음/없음 두 가지로 추정함

본 모델은 단일 문장 내에 있는 사건 단어(Event Word)와 시간 표현(Temporal Expression)간의 관계를 추정하기 위한 모델임
모델의 입력으로 사건 단어와 시간 표현의 최단 의존성 경로(Shortest Dependency Path)에 있는 단어들과 각 단어들의 엔티티 정보, 단어 임베딩 벡터, 의존성 정보, 품사 정보가 주어짐


> <b><h4> 샘플 데이터 </h4></b>

샘플 데이터 경로 : data/sample_original/

샘플 데이터 형태(Json Type)
-text : 입력되는 단일 문장
-tlink : 사건 단어-시간 표현 쌍


> <b><h4> 전처리(Preprocess) </h4></b>

명령어 
- original_path : 원본 파일 경로(샘플 데이터 형태)
- preprocess_path : Shortest Path에 있는 E-T 쌍
- output_file : 모델에 입력으로 들어갈 문서

<pre>
<code> python preprocess.py original_path preprocess_path output_file</code>
</pre>


> <b><h4>기훈련 모델 사용방법(How to used Pretrained Model)</h4></b>

Input : Entity 정보(3-dim) + 단어 임베딩(200-dim) + Dependency Relation(19-dim) + POS 정보(45-dim)
 - 1줄에 한 쌍, file 1개
 - Entity 정보 (one-hot vector) : 사건 단어일 경우 <1, 0, 0>, 시간 표현일 경우 <0, 1, 0>, 그 외일 경우 <0, 0, 1>
 
Output : 원본 문서(Json, 한 문서 당 1개)
 - etlink : 사건 단어와 시간 표현 간에 관계성이 있는 쌍 번호
 - text : 입력 문장 원문
 - tlink : 추정하려는 t-link 쌍

명령어
 - model :  기학습된 모델 경로
 - input : 모델에 입력될 경로
 - input_json : 전처리에서 preprocess_path에 해당하는 경로
 - output : 모델 실험 결과
 - output_json : 모델 실험 결과를 json 형태로 변환
 
<pre>
<code> python predict_json.py -model model_path -input input_path -input_json original_json_path -out_name output_path -out_json output_type_json</code>
</pre><br/>
