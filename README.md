<H3> 한국어 사건 단어-시간 표현 관계 추정 모델 </H3>  

---
  

![model](https://user-images.githubusercontent.com/37574306/58693490-debc6880-83cb-11e9-8ed6-2abbddd19655.png)

주어진 문장과 문장 내 사건 단어와 시간 표현 간의 관계 유무 추정 모델 코드  
관계 추정은 둘의 관계가 있음/없음 두 가지로 추정함

> <b><h4> 전처리(Preprocess) </h4></b>

여러 파일을 하나로 합침

<pre>
<code> python maketestdataone.py input_path output_file.txt</code>
</pre>


> <b><h4>기훈련 모델 사용방법(How to used Pretrained Model)</h4></b>

Input : Entity 정보(3-dim) + 단어 임베딩(200-dim) + Dependency Parsing(19-dim) + POS 정보(45-dim)
 - 1줄에 한 쌍, file 1개
Output : 원본 문서(Json, 한 문서 당 1개)
 - etlink : 사건 단어와 시간 표현 간에 관계성이 있는 쌍 번호
 - text : 입력 문장 원문
 - tlink : 추정하려는 t-link 쌍

<pre>
<code> python predict_json.py -model model_path -input input_path -input_json original_json_path -out_name output_path -out_json output_type_json</code>
</pre><br/>
