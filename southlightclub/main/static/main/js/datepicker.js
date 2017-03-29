// Date picker
$(document).ready(function() {
  
  // If mobile, use device's default datepicker, else use jQuery's datepicker.
  if (typeof window.orientation !== 'undefined') {  // Mobile device
    $('input.datepicker').attr('type', 'date');
    $('input.datepicker').removeClass('datepicker').remove('hasDatepicker').remove('dateWidth');
    return;
  }
  
  $.datepicker.regional['zh-TW'] = {
    clearText: '清除',
    clearStatus: '清除已選日期',
    closeText: '關閉',
    closeStatus: '取消選擇',
    prevText: '<上一月',
    prevStatus: '顯示上個月',
    nextText: '下一月>',
    nextStatus: '顯示下個月',
    currentText: '今天',
    currentStatus: '顯示本月',
    monthNames: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
    monthNamesShort: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
    monthStatus: '選擇月份',
    yearStatus: '選擇年份',
    weekHeader: '周',
    weekStatus: '',
    dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
    dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
    dayNamesMin: ['日','一','二','三','四','五','六'],
    dayStatus: '設定每周第一天',
    dateStatus: '選擇 m月 d日, DD',
    dateFormat: 'yy/mm/dd',
    firstDay: 1, 
    initStatus: '請選擇日期',
    isRTL: false
  };
  var dateToday = new Date();
  var yearRange = (dateToday.getFullYear() - 100) + ":" + (dateToday.getFullYear() + 100);
  $('.datepicker').datepicker({
    dateFormat : 'yy-mm-dd',
    changeMonth : true,
    changeYear : true,
    yearRange: yearRange,
  });
  $.datepicker.setDefaults($.datepicker.regional['zh-TW']);
  
});
