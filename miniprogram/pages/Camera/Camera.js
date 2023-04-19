// pages/Camera/Camera.js
const app=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    src:"",
    flag:0
  },

  takePhoto(){
    const ctx=wx.createCameraContext()
    ctx.takePhoto({
      quality:'high',
      success:(res)=>{
        this.setData({
          src:res.tempImagePath,
          flag:1
        })
      }
    })
  },

  upload(param){
    var src=param.detail.value.imagesrc
    app.globalData.src=src
    //console.log(app.globalData.src)
    //console.log(src)
    wx.showToast({
      title: '正在识别',
      icon: 'loading'
    }),
    wx.uploadFile({
      filePath: src,
      name: 'photo',
      url: 'http://localhost:5000/emotion',
      success:function(res){
        //console.log(res.data)
        //返回的是json格式的数据，需要转码
        var json1 = JSON.parse(res.data);
        var flag = json1['flag']
        if(flag==0){
          wx.showModal({
            cancelColor: 'cancelColor',
            content: '当前图片未检测到人脸，请重新上传！',
            title: '提示'
          })
        }
        else{
          app.globalData.angry=json1['angry']
          app.globalData.disgust=json1['disgust']
          app.globalData.happy=json1['happy']
          app.globalData.neutral=json1['neutral']
          app.globalData.fear=json1['fear']
          app.globalData.sad=json1['sad']
          app.globalData.surprise=json1['surprise']
          app.globalData.emotion=json1['emotion_text']
          wx.showToast({
            title: '上传成功！',   
            duration: 1000,
            success:function(){
              setTimeout(function(){
                wx.navigateTo({
                  url: '/pages/Result/Result',
                })
              },1000)
            }
          })
        }
      }
    })
  },

  retake(){
    this.setData({
      flag:0,
      src:""
    })
  },

  error(e){
    console.log(e.detail)
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

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