// pages/Result/Result.js
var wxCharts = require('../../utils/wxcharts');
var app = getApp();
var columnChart = null;

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isMainChartDisplay: true,
  },

  onReady: function (e) {
    this.setData({
      emotion:app.globalData.emotion,
      src:app.globalData.src
    })
    var chartData = {
      main: {
          title: '订单统计',
          data: [app.globalData.angry, app.globalData.disgust, app.globalData.fear, app.globalData.happy, app.globalData.sad, app.globalData.surprise, app.globalData.neutral],
          categories: ['生气', '厌恶', '害怕', '开心', '伤心', '惊讶', '中性']
      }    
    };
    var windowWidth = 400;
    try {
      var res = wx.getSystemInfoSync();
      windowWidth = res.windowWidth;
    } catch (e) {
      console.error('getSystemInfoSync failed!');
    }

    columnChart = new wxCharts({
      canvasId: 'columnCanvas',
      type: 'column',
      animation: true,
      categories: ['生气', '厌恶', '害怕', '开心', '伤心', '惊讶', '中性'],
      series: [{
          data: chartData.main.data,
          format: function (val, name) {
              return parseFloat(val).toFixed(2) + '%';
          }
      }],
      yAxis: {
        format: function (val) {
            return val + '%';
        },
        min: 0
    },
      xAxis: {
          disableGrid: false,
          type: 'calibration'
      },
      extra: {
          column: {
              width: 20,
          },
          legendTextColor: '#188df0'
      },
      width: windowWidth,
      height: 180,
    });
  },

  backtoindex(){
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})