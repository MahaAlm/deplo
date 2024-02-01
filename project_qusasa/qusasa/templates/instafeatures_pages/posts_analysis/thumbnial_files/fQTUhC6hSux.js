;/*FB_PKG_DELIM*/

__d("IGDSContextMenuHeader.react",["IGDSChevronIcon","IGDSIconButton.react","IGDSListItem.react","IGDSText.react","PolarisGenericStrings","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i=(h||(h=d("react"))).unstable_useMemoCache,j=h,k={border:{borderBottomColor:"x1xp9za0",borderBottomStyle:"x1q0q8m5",borderBottomWidth:"x1co6499",$$css:!0},button:{height:"xxk0z11",marginTop:"xifccgj",marginEnd:"xykv574",marginBottom:"x4cne27",marginStart:"xbmpl8g",width:"xvy4d1p",$$css:!0}};function a(a){var b=i(9),e=a.icon,f=a.label;a=a.onReturn;e=(e=e)!=null?e:void 0;var g;b[0]===Symbol["for"]("react.memo_cache_sentinel")?(g=j.jsx(c("IGDSChevronIcon"),{alt:d("PolarisGenericStrings").BACK_TEXT,color:"ig-tertiary-icon",direction:"back",size:12}),b[0]=g):g=b[0];b[1]!==a?(g=j.jsx(c("IGDSIconButton.react"),{onClick:a,padding:0,xstyle:k.button,children:g}),b[1]=a,b[2]=g):g=b[2];b[3]!==f?(a=j.jsx(c("IGDSText.react"),{maxLines:1,size:"label",weight:"semibold",zeroMargin:!0,children:f}),b[3]=f,b[4]=a):a=b[4];b[5]!==e||b[6]!==g||b[7]!==a?(f=j.jsx(c("IGDSListItem.react"),{addOnEnd:e,addOnStart:g,backgroundColor:"ig-banner-background",cursorDisabled:!0,paddingY:4,title:a,xstyle:k.border}),b[5]=e,b[6]=g,b[7]=a,b[8]=f):f=b[8];return f}g["default"]=a}),98);
__d("IGDSContextMenuPushPage.react",["react"],(function(a,b,c,d,e,f,g){"use strict";var h,i=(h||(h=d("react"))).unstable_useMemoCache,j=h;function a(a){var b=i(8),c=a.children,d=a.footer;a=a.header;var e;b[0]===Symbol["for"]("react.memo_cache_sentinel")?(e="xgf5ljw x78zum5 xdt5ytf xmz0i5r",b[0]=e):e=b[0];var f;b[1]===Symbol["for"]("react.memo_cache_sentinel")?(f="xgf5ljw x1iyjqo2 x1odjw0f x1y1aw1k x1sxyh0 xwib8y2 xurb0ha",b[1]=f):f=b[1];b[2]!==c?(f=j.jsx("div",{className:f,children:c}),b[2]=c,b[3]=f):f=b[3];c=d!=null&&d;b[4]!==a||b[5]!==f||b[6]!==c?(d=j.jsxs("div",{className:e,children:[a,f,c]}),b[4]=a,b[5]=f,b[6]=c,b[7]=d):d=b[7];return d}g["default"]=a}),98);
__d("IGDSContextMenuPushPageListItem.react",["IGDSListItem.react","IGDSText.react","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i=(h||(h=d("react"))).unstable_useMemoCache,j=h,k={hoverOverlay:{backgroundColor:"xks8skl",$$css:!0}};function a(a){var b=i(8),d=a.addOnEnd,e=a.addOnStart,f=a.linkProps,g=a.onPress;a=a.title;var h;b[0]!==a?(h=j.jsx(c("IGDSText.react"),{maxLines:1,zeroMargin:!0,children:a}),b[0]=a,b[1]=h):h=b[1];b[2]!==d||b[3]!==e||b[4]!==f||b[5]!==g||b[6]!==h?(a=j.jsx(c("IGDSListItem.react"),{addOnEnd:d,addOnStart:e,backgroundColor:"ig-banner-background",linkProps:f,onPress:g,overlayDisabled:!1,overlayHoveredStyle:k.hoverOverlay,overlayRadius:8,paddingY:4,title:h}),b[2]=d,b[3]=e,b[4]=f,b[5]=g,b[6]=h,b[7]=a):a=b[7];return a}g["default"]=a}),98);
__d("PolarisSwitchAppearancePushPage.react",["fbt","IGDSAdjustmentBrightnessPanoOutlineIcon","IGDSContextMenuHeader.react","IGDSContextMenuItem.react","IGDSContextMenuPushPage.react","IGDSContextMenuPushPageListItem.react","IGDSMoonPanoOutlineIcon","IGDSSwitch.react","InstagramODS","PolarisIGTheme.react","PolarisLogger","PolarisThemeStrings","react"],(function(a,b,c,d,e,f,g,h){"use strict";var i,j=(i||(i=d("react"))).unstable_useMemoCache,k=i;function a(a){var b=j(15);a=a.onReturn;var e=d("PolarisIGTheme.react").useTheme(),f=e.getTheme();f=f===d("PolarisIGTheme.react").IGTheme.Dark;var g;b[0]!==e?(g=function(){e.toggleTheme(),c("InstagramODS").incr("web.nav.toggle_theme_click"),d("PolarisLogger").logAction("appThemeToggled")},b[0]=e,b[1]=g):g=b[1];g=g;var i;b[2]!==f?(i=f?k.jsx("div",{className:"xs4xyr0 x127lhb5",children:k.jsx(c("IGDSMoonPanoOutlineIcon"),{alt:h._("__JHASH__YRjaSdy6a7n__JHASH__"),size:d("IGDSContextMenuItem.react").ICON_SIZE})},"darkMode"):k.jsx("div",{className:"xs4xyr0 x127lhb5",children:k.jsx(c("IGDSAdjustmentBrightnessPanoOutlineIcon"),{alt:h._("__JHASH__YRjaSdy6a7n__JHASH__"),size:d("IGDSContextMenuItem.react").ICON_SIZE})},"lightMode"),b[2]=f,b[3]=i):i=b[3];i=i;var l;b[4]!==i||b[5]!==a?(l=k.jsx(c("IGDSContextMenuHeader.react"),{icon:i,label:d("PolarisThemeStrings").SWITCH_APPEARANCE_TEXT,onReturn:a}),b[4]=i,b[5]=a,b[6]=l):l=b[6];b[7]!==f?(i=k.jsx(c("IGDSSwitch.react"),{size:"small",value:f}),b[7]=f,b[8]=i):i=b[8];b[9]!==i||b[10]!==g?(a=k.jsx(c("IGDSContextMenuPushPageListItem.react"),{addOnEnd:i,onPress:g,title:d("PolarisThemeStrings").DARK_MODE_TEXT}),b[9]=i,b[10]=g,b[11]=a):a=b[11];b[12]!==l||b[13]!==a?(f=k.jsx(c("IGDSContextMenuPushPage.react"),{header:l,children:a}),b[12]=l,b[13]=a,b[14]=f):f=b[14];return f}g["default"]=a}),98);
__d("BizSuiteCoreGrowthInstagramWebEntryPointClickFalcoEvent",["FalcoLoggerInternal","getFalcoLogPolicy_DO_NOT_USE"],(function(a,b,c,d,e,f,g){"use strict";a=c("getFalcoLogPolicy_DO_NOT_USE")("4805");b=d("FalcoLoggerInternal").create("biz_suite_core_growth_instagram_web_entry_point_click",a);e=b;g["default"]=e}),98);
__d("BizSuiteCoreGrowthInstagramWebEntryPointImpressionFalcoEvent",["FalcoLoggerInternal","getFalcoLogPolicy_DO_NOT_USE"],(function(a,b,c,d,e,f,g){"use strict";a=c("getFalcoLogPolicy_DO_NOT_USE")("4807");b=d("FalcoLoggerInternal").create("biz_suite_core_growth_instagram_web_entry_point_impression",a);e=b;g["default"]=e}),98);