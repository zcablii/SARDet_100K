## SARDet-100K: Towards Open-Source Benchmark and ToolKit for Large-Scale SAR Object Detection" at: [https://arxiv.org/pdf/2403.06534.pdf](https://arxiv.org/pdf/2403.06534.pdf)


![MSFA](MSFA/docs/SARDet100K_samples.png)

## Abstract

Synthetic Aperture Radar (SAR) object detection has gained significant attention recently due to its irreplaceable all-weather imaging capabilities. However, this research field suffers from both limited public datasets (mostly comprising <2K images with only mono-category objects) and inaccessible source code. To tackle these challenges, we establish a new benchmark dataset and an open-source method for large-scale SAR object detection. Our dataset, SARDet-100K, is a result of intense surveying, collecting, and standardizing 10 existing SAR detection datasets, providing a large-scale and diverse dataset for research purposes. To the best of our knowledge, SARDet-100K is the first COCO-level large-scale multi-class SAR object detection dataset ever created. With this high-quality dataset, we conducted comprehensive experiments and uncovered a crucial challenge in SAR object detection: the substantial disparities between the pretraining on RGB datasets and finetuning on SAR datasets in terms of both data domain and model structure. To bridge these gaps, we propose a novel Multi-Stage with Filter Augmentation (MSFA) pretraining framework that tackles the problems from the perspective of data input, domain transition, and model migration. The proposed MSFA method significantly enhances the performance of SAR object detection models while demonstrating exceptional generalizability and flexibility across diverse models. This work aims to pave the way for further advancements in SAR object detection. 


![MSFA](MSFA/docs/SARDet100K.png)

## Introduction

This repository is the official site for "SARDet-100K: Towards Open-Source Benchmark and ToolKit for Large-Scale SAR Object Detection" 
at: [https://arxiv.org/pdf/2403.06534.pdf](https://arxiv.org/pdf/2403.06534.pdf)

**DATASET DOWNLOAD at:** 

* Baidu Disk: [Dataset](https://pan.baidu.com/s/1dIFOm4V2pM_AjhmkD1-Usw?pwd=SARD)
* OneDrive: [Images](https://liveuclac-my.sharepoint.com/:f:/g/personal/zcablii_ucl_ac_uk/EutczQ-0LB5BmQ1BEguS-PAB8mLXUChRWPVY2Bn5X4-0_w?e=bxPZij), [Annotations](https://liveuclac-my.sharepoint.com/:f:/g/personal/zcablii_ucl_ac_uk/ElrfZN95SUpPmT9YlvRCV7YBF7-cOuVJlRXJXO9-Y4S9CQ?e=3m00JW)

**(Only Train and Val sets are released so far.)**


<table style="border-collapse: collapse; border: none; border-spacing: 0px;">
	<caption>
		Image and instance level statistics of SARDet-100K dataset. *: Origin datasets are cropped into 512 x 512 patches.
	</caption>
	<tr>
		<td rowspan="2" style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			 <b>Dataset</b>
		<td colspan="4" style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			 <b>Images</b>
		<td colspan="4" style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			<b>Instances</b>
		<td rowspan="2" style="border-bottom: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			Ins/Img
	<tr>
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			Train
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			Val
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			Test
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			ALL
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			Train
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			Val
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			Test
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			ALL
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			AIR_SARShip 1*&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			438
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			23
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			40
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			501
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			816
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			33
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			209
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,058
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			2.11
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			AIR_SARShip 2&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			270
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			15
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			15
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			300
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,819
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			127
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			94
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			2,040
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			6.80
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			HRSID&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			3,642
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			981
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			981
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			5,604
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			11,047
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			2,975
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			2,947
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			16,969
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			3.03
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			MSAR*&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			27,159
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,479
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,520
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			30,158
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			58,988
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			3,091
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			3,123
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			65,202
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			2.16
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			SADD&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			795
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			44
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			44
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			883
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			6,891
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			448
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			496
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			7,835
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			8.87
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			SAR-AIRcraft*&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			13,976
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,923
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			2,989
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			18,888
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			27,848
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			4,631
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			5,996
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			38,475
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			2.04
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			ShipDataset&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			31,784
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			3,973
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			3,972
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			39,729
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			40,761
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			5,080
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			5,044
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			50,885
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			1.28
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			SSDD&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			928
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			116
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			116
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,160
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			2,041
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			252
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			294
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			2,587
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			2.23
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			OGSOD&nbsp;
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			14,664
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,834
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,833
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			18,331
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			38,975
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			4,844
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			4,770
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			48,589
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			2.65
	<tr>
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			SIVED&nbsp;
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			837
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			104
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			103
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,044
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			9,561
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,222
		<td style="border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			1,230
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			12,013
		<td style="border-bottom: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			11.51&nbsp;
	<tr>
		<td style="border-right: 1px solid black; text-align: center; padding-right: 3pt; padding-left: 3pt;">
			<b>SARDet-100k</b>
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			94,493
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			10,492
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			11,613
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			116,598
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			198,747
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			22,703
		<td style="text-align: right; padding-right: 3pt; padding-left: 3pt;">
			24,023
		<td style="border-right: 1px solid black; text-align: right; padding-right: 3pt; padding-left: 3pt;">
			245,653
		<td style="text-align: center; padding-right: 3pt; padding-left: 3pt;">
			2.11
</table>





<table style="border-collapse: collapse; border: none; border-spacing: 0px;">
	<caption>
		SARDet-100K source datasets information. GF-3: Gaofen-3, S-1: Sentinel-1. Target categories S: ship, A: aircraft, C: car, B: bridge, H: harbour, T: tank.
	</caption>
	<tr>
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Datasets
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Target
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Res.&nbsp;(m)
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Band
		<td style="border-right: 1px solid black; border-bottom: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Polarization
		<td style="border-bottom: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Satellites
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			AIR_SARShip
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			S
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			1,3m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			VV
		<td style="padding-right: 3pt; padding-left: 3pt;">
			GF-3
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			HRSID
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			S
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			0.5~3m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C/X
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			HH, HV, VH, VV
		<td style="padding-right: 3pt; padding-left: 3pt;">
			S-1B,TerraSAR-X,TanDEMX
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			MSAR
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			A, T, B, S
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			&lt; 1m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			HH, HV, VH, VV
		<td style="padding-right: 3pt; padding-left: 3pt;">
			HISEA-1
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			SADD
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			A
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			0.5~3m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			X
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			HH
		<td style="padding-right: 3pt; padding-left: 3pt;">
			TerraSAR-X
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			SAR-AIRcraft
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			A
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			1m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Uni-polar
		<td style="padding-right: 3pt; padding-left: 3pt;">
			GF-3
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			ShipDataset
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			S
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			3~25m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			HH, VV, VH, HV
		<td style="padding-right: 3pt; padding-left: 3pt;">
			S-1,GF-3
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			SSDD
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			S
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			1~15m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C/X
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			HH, VV, VH, HV
		<td style="padding-right: 3pt; padding-left: 3pt;">
			S-1,RadarSat-2,TerraSAR-X
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			OGSOD
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			B, H, T
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			3m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			VV/VH
		<td style="padding-right: 3pt; padding-left: 3pt;">
			GF-3
	<tr>
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			SIVED
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			C
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			0.1,0.3m
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			Ka,Ku,X
		<td style="border-right: 1px solid black; padding-right: 3pt; padding-left: 3pt;">
			VV/HH
		<td style="padding-right: 3pt; padding-left: 3pt;">
			Airborne SAR synthetic slice
</table>


## Acknowledgement



## Citation

If you use this toolbox or benchmark in your research, please cite this project.

```bibtex
@article{li2024sardet100k,
      title={SARDet-100K: Towards Open-Source Benchmark and ToolKit for Large-Scale SAR Object Detection}, 
      author={Yuxuan Li and Xiang Li and Weijie Li and Qibin Hou and Li Liu and Ming-Ming Cheng and Jian Yang},
      year={2024},
      journal={arXiv},
}
```

## License

This project is released under the [Attribution-NonCommercial 4.0 International](LICENSE).

 