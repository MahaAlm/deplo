;/*FB_PKG_DELIM*/

__d("PolarisSuggestedUserListQuery$Parameters",[],(function(a,b,c,d,e,f){"use strict";a={kind:"PreloadableConcreteRequest",params:{id:"6934450413267510",metadata:{},name:"PolarisSuggestedUserListQuery",operationKind:"query",text:null}};e.exports=a}),null);
__d("PolarisFeedTimelineRootV2Query$Parameters",[],(function(a,b,c,d,e,f){"use strict";a={kind:"PreloadableConcreteRequest",params:{id:"7313479825382223",metadata:{},name:"PolarisFeedTimelineRootV2Query",operationKind:"query",text:null}};e.exports=a}),null);
__d("PolarisPanavisionFeedRoot.entrypoint",["JSResourceForInteraction","PolarisFeedTimelineRootV2Query$Parameters","PolarisFeedVariants","PolarisSuggestedUserListQuery$Parameters","gkx"],(function(a,b,c,d,e,f,g){"use strict";a={getPreloadProps:function(a){var b=a.routeParams;a=a.routeProps;var d=c("PolarisFeedVariants").cast(b.variant);d=d!=null&&d!=="home"?{pagination_source:String(d)}:{};return{queries:babelHelpers["extends"]({polarisFeedTimelineQuery:{options:{},parameters:c("PolarisFeedTimelineRootV2Query$Parameters"),variables:{data:babelHelpers["extends"]({},d,{device_id:a.device_id,is_async_ads_double_request:"0",is_async_ads_in_headload_enabled:"0",is_async_ads_rti:"0",rti_delivery_backend:"0"}),variant:(d=b.variant)!=null?d:String("home")}}},c("gkx")("9827")?{polarisSuggestedUserListQuery:{options:{},parameters:c("PolarisSuggestedUserListQuery$Parameters"),variables:{data:{max_id:"",max_number_to_display:5,module:"discover_people",paginate:!0}}}}:void 0)}},root:c("JSResourceForInteraction")("PolarisFeedRoot.next.react").__setRef("PolarisPanavisionFeedRoot.entrypoint")};g["default"]=a}),98);
__d("PolarisOrdersAndPaymentsSubscriptionsRootQuery_instagramRelayOperation",[],(function(a,b,c,d,e,f){e.exports="24280272041564258"}),null);