1. 检查通过率和阈值

   * 主要查看`prod_ml_pos.pass_rate_thresholds`是否异常（15%和3%是否存在显著差异）
   * prod_ml_pos.pass_rate_thresholds_updates的app_count快到windows值时

2. 3%坏帐统计跟踪

   * 在120.26.2.230:/home/weill/log/notebook/bad_rate_compare.ipynb中包括3%和15%/rc的坏帐比较，目前使用fpd7

3. 定时模型训练

   * 114.55.108.15上定时模型训练，下一次是11.27

4. 定时数据采集

   * 114.55.108.15上定时数据采集

5. 定时报告

   - 已经改成了linux crontab，定时任务见：http://confluence.win.fenqi.im/pages/viewpage.action?pageId=12003617

   ​

