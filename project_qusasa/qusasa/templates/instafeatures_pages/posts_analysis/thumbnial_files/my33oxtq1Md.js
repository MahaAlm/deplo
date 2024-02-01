;/*FB_PKG_DELIM*/

__d("PolarisMobilePostCaptionFragment.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisMobilePostCaptionFragment",selections:[{alias:null,args:null,concreteType:"XDTUserDict",kind:"LinkedField",name:"user",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"is_verified",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"pk",storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"XDTCommentDict",kind:"LinkedField",name:"caption",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"text",storageKey:null}],storageKey:null}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("PolarisMobilePostDetailsSectionFragment.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisMobilePostDetailsSectionFragment",selections:[{kind:"RequiredField",field:{alias:null,args:null,kind:"ScalarField",name:"code",storageKey:null},action:"THROW",path:"code"},{alias:null,args:null,kind:"ScalarField",name:"taken_at",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"comment_count",storageKey:null},{alias:null,args:null,concreteType:"XDTCommentDict",kind:"LinkedField",name:"comments",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null},{args:null,kind:"FragmentSpread",name:"PolarisPostUFI_media"},{args:null,kind:"FragmentSpread",name:"PolarisPostFastViewAllComments_media"},{args:null,kind:"FragmentSpread",name:"PolarisMobilePostCaptionFragment"},{args:null,kind:"FragmentSpread",name:"PolarisMobilePostPreviewCommentsFragment"},{args:null,kind:"FragmentSpread",name:"PolarisPostFooterFragment_media"}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("PolarisMobilePostFragment.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisMobilePostFragment",selections:[{args:null,kind:"FragmentSpread",name:"PolarisMedia_media"},{args:null,kind:"FragmentSpread",name:"PolarisMobilePostDetailsSectionFragment"},{args:null,kind:"FragmentSpread",name:"PolarisPostHeaderLegacyContainer_media"},{args:null,kind:"FragmentSpread",name:"usePolarisMediaInitialCarouselIndex"},{args:null,kind:"FragmentSpread",name:"usePolarisPostViewpointLogging"},{args:null,kind:"FragmentSpread",name:"PolarisPostContextFragment"}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("PolarisMobilePostPreviewCommentsFragment.graphql",[],(function(a,b,c,d,e,f){"use strict";a=function(){var a={alias:null,args:null,kind:"ScalarField",name:"pk",storageKey:null};return{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisMobilePostPreviewCommentsFragment",selections:[{kind:"RequiredField",field:a,action:"THROW",path:"pk"},{alias:null,args:null,concreteType:"XDTCommentDict",kind:"LinkedField",name:"comments",plural:!0,selections:[{kind:"RequiredField",field:a,action:"THROW",path:"comments.pk"},{alias:null,args:null,kind:"ScalarField",name:"text",storageKey:null},{alias:null,args:null,concreteType:"XDTUserDict",kind:"LinkedField",name:"user",plural:!1,selections:[{kind:"RequiredField",field:a,action:"THROW",path:"comments.user.pk"},{alias:null,args:null,kind:"ScalarField",name:"is_verified",storageKey:null},{kind:"RequiredField",field:{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},action:"THROW",path:"comments.user.username"}],storageKey:null},{args:null,kind:"FragmentSpread",name:"PolarisCommentLikeButton_comment"}],storageKey:null}],type:"XDTMediaDict",abstractKey:null}}();e.exports=a}),null);
__d("usePolarisMediaInitialCarouselIndex.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"usePolarisMediaInitialCarouselIndex",selections:[{alias:null,args:null,kind:"ScalarField",name:"main_feed_carousel_starting_media_id",storageKey:null},{alias:null,args:null,concreteType:"XDTMediaDict",kind:"LinkedField",name:"carousel_media",plural:!0,selections:[{kind:"RequiredField",field:{alias:null,args:null,kind:"ScalarField",name:"pk",storageKey:null},action:"THROW",path:"carousel_media.pk"}],storageKey:null}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("usePolarisPostViewpointLogging.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"usePolarisPostViewpointLogging",selections:[{kind:"RequiredField",field:{alias:null,args:null,kind:"ScalarField",name:"pk",storageKey:null},action:"THROW",path:"pk"},{args:null,kind:"FragmentSpread",name:"PolarisOrganicImpressionAction_media"},{args:null,kind:"FragmentSpread",name:"PolarisVpvdImpressionActionForPost_media"}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("PolarisPostHeaderLegacyContainer_ad.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisPostHeaderLegacyContainer_ad",selections:[{alias:null,args:null,kind:"ScalarField",name:"ad_title",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"display_fb_page_name",storageKey:null},{args:null,kind:"FragmentSpread",name:"PolarisPostFastOptionsButton_ad"}],type:"XDTAdInsertionItemClientDict",abstractKey:null};e.exports=a}),null);
__d("PolarisPostHeaderLegacyContainer_media.graphql",[],(function(a,b,c,d,e,f){"use strict";a=function(){var a={alias:null,args:null,kind:"ScalarField",name:"pk",storageKey:null};return{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisPostHeaderLegacyContainer_media",selections:[{kind:"RequiredField",field:a,action:"THROW",path:"pk"},{alias:null,args:null,kind:"ScalarField",name:"media_type",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"is_paid_partnership",storageKey:null},{alias:null,args:null,concreteType:"XDTAffiliateInfo",kind:"LinkedField",name:"affiliate_info",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"disclosure_tag",storageKey:null}],storageKey:null},{kind:"RequiredField",field:{alias:null,args:null,concreteType:"XDTUserDict",kind:"LinkedField",name:"owner",plural:!1,selections:[{kind:"RequiredField",field:a,action:"THROW",path:"owner.pk"},{alias:null,args:null,concreteType:"XDTGroupMetadata",kind:"LinkedField",name:"group_metadata",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"is_group",storageKey:null}],storageKey:null}],storageKey:null},action:"THROW",path:"owner"},{args:null,kind:"FragmentSpread",name:"PolarisPostFastOptionsButton_media"},{args:null,kind:"FragmentSpread",name:"PolarisPostHeaderFavoritedIconButton_items"}],type:"XDTMediaDict",abstractKey:null}}();e.exports=a}),null);
__d("PolarisPostPageMetadataFragment.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisPostPageMetadataFragment",selections:[{alias:null,args:null,concreteType:"XDTCommentDict",kind:"LinkedField",name:"caption",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"text",storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"XDTUserDict",kind:"LinkedField",name:"owner",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"full_name",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"media_type",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"product_type",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"taken_at",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"title",storageKey:null}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("PolarisPostPageWrapperFragment.graphql",[],(function(a,b,c,d,e,f){"use strict";a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"PolarisPostPageWrapperFragment",selections:[{kind:"RequiredField",field:{alias:null,args:null,kind:"ScalarField",name:"pk",storageKey:null},action:"THROW",path:"pk"},{args:null,kind:"FragmentSpread",name:"PolarisPostPageMetadataFragment"}],type:"XDTMediaDict",abstractKey:null};e.exports=a}),null);
__d("withPolarisShell",["PolarisShell.react","react","usePolarisPageID"],(function(a,b,c,d,e,f,g){"use strict";var h,i=h||d("react");function a(a,b){b===void 0&&(b={});function d(d){var e=c("usePolarisPageID")();return i.jsx(c("PolarisShell.react"),babelHelpers["extends"]({},b,{pageIdentifier:e,children:i.jsx(a,babelHelpers["extends"]({},d))}))}d.displayName=d.name+" [from "+f.id+"]";return d}g["default"]=a}),98);
__d("PolarisMobilePostCaption.next.react",["CometRelay","PolarisMobilePostCaptionFragment.graphql","PolarisPostFastCommentPrimitive.react","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=(i||(i=d("react"))).unstable_useMemoCache,k=i;function a(a){var e,f=j(12);a=a.queryReference;a=d("CometRelay").useFragment(h!==void 0?h:h=b("PolarisMobilePostCaptionFragment.graphql"),a);if(f[0]!==a.user){var g;g=(g=a.user)==null?void 0:g.username;f[0]=a.user;f[1]=g}else g=f[1];g=g;if(f[2]!==a.user){var i;i=(i=a.user)==null?void 0:i.pk;f[2]=a.user;f[3]=i}else i=f[3];i=i;e=((e=a.user)==null?void 0:e.is_verified)===!0;if(f[4]!==a.caption){var l;l=(l=a.caption)==null?void 0:l.text;f[4]=a.caption;f[5]=l}else l=f[5];a=l;if(g==null||i==null||a==null)return null;f[6]===Symbol["for"]("react.memo_cache_sentinel")?(l="x12nagc",f[6]=l):l=f[6];f[7]!==e||f[8]!==a||f[9]!==i||f[10]!==g?(l=k.jsx("div",{className:l,children:k.jsx(c("PolarisPostFastCommentPrimitive.react"),{isAuthorVerified:e,isCaption:!0,text:a,userId:i,username:g})}),f[7]=e,f[8]=a,f[9]=i,f[10]=g,f[11]=l):l=f[11];return l}g["default"]=a}),98);
__d("PolarisMobilePostPreviewComments.next.react",["CometRelay","IGDSBox.react","PolarisCommentLikeButton.next.react","PolarisMobilePostPreviewCommentsFragment.graphql","PolarisPostFastCommentPrimitive.react","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=(i||(i=d("react"))).unstable_useMemoCache,k=i;function a(a){var e=j(4);a=a.queryReference;a=d("CometRelay").useFragment(h!==void 0?h:h=b("PolarisMobilePostPreviewCommentsFragment.graphql"),a);if(a.comments==null||a.comments.length===0)return null;var f;e[0]!==a.comments?(f=a.comments.map(function(a){return a.user!=null&&a.text!=null&&k.jsxs(c("IGDSBox.react"),{alignItems:"center",direction:"row",display:"flex",marginBottom:1,children:[k.jsx(c("PolarisPostFastCommentPrimitive.react"),{isAuthorVerified:a.user.is_verified===!0,text:a.text,userId:a.user.pk,username:a.user.username}),k.jsx(c("PolarisCommentLikeButton.next.react"),{isLarge:!1,queryReference:a})]},a.pk)}),e[0]=a.comments,e[1]=f):f=e[1];e[2]!==f?(a=k.jsx(c("IGDSBox.react"),{children:f}),e[2]=f,e[3]=a):a=e[3];return a}g["default"]=a}),98);
__d("PolarisMobilePostDetailsSection.next.react",["CometRelay","IGDSBox.react","PolarisMobilePostCaption.next.react","PolarisMobilePostDetailsSectionFragment.graphql","PolarisMobilePostPreviewComments.next.react","PolarisPostFastViewAllComments.next.react","PolarisPostFooter.next.react","PolarisPostTimestamp.react","PolarisPostUFI.next.react","PolarisSponsoredPostContext.react","XPolarisMobileAllCommentsControllerRouteBuilder","react","useCometRouterDispatcher","usePolarisViewer"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=i||(i=d("react"));e=i;e.useCallback;var k=e.useContext,l=e.unstable_useMemoCache,m={likeButton:{marginStart:"xp7jhwk",marginLeft:null,marginRight:null,$$css:!0},mainContent:{display:"x78zum5",flexDirection:"xdt5ytf",paddingTop:"x1yrsyyn",paddingEnd:"x1pi30zi",paddingBottom:"x1l90r2v",paddingStart:"x1swvt13",$$css:!0},socialProof:{marginBottom:"x1e56ztr",marginTop:"x1xmf6yo",$$css:!0},ufi:{marginTop:"x1gslohp",$$css:!0}};function a(a){var e=l(34);a=a.queryReference;var f=d("CometRelay").useFragment(h!==void 0?h:h=b("PolarisMobilePostDetailsSectionFragment.graphql"),a);a=c("usePolarisViewer")();var g=k(d("PolarisSponsoredPostContext.react").PolarisSponsoredPostContext),i=g.canUserSeePersistentCta,n=c("useCometRouterDispatcher")();e[0]!==i||e[1]!==f.code||e[2]!==n?(g=function(){var a=c("XPolarisMobileAllCommentsControllerRouteBuilder").buildURL({enable_persistent_cta:i,shortcode:f.code});n==null?void 0:n.go(a,{})},e[0]=i,e[1]=f.code,e[2]=n,e[3]=g):g=e[3];g=g;var o=Number(f.taken_at),p=f.comment_count!=null&&f.comments!=null&&f.comment_count>f.comments.length,q;e[4]!==f?(q=j.jsx(c("PolarisPostFooter.next.react"),{analyticsContext:"postPage",queryReference:f}),e[4]=f,e[5]=q):q=e[5];var r;e[6]===Symbol["for"]("react.memo_cache_sentinel")?(r="x78zum5 xdt5ytf x1yrsyyn x1pi30zi x1l90r2v x1swvt13",e[6]=r):r=e[6];var s;e[7]===Symbol["for"]("react.memo_cache_sentinel")?(s="x1gslohp",e[7]=s):s=e[7];e[8]!==f||e[9]!==g||e[10]!==a?(s=j.jsx("div",{className:s,children:j.jsx(c("PolarisPostUFI.next.react"),{adQueryReference:null,likeButtonXStyle:m.likeButton,mediaQueryReference:f,onCommentButtonClick:g,socialProofXStyle:m.socialProof,viewer:a})}),e[8]=f,e[9]=g,e[10]=a,e[11]=s):s=e[11];e[12]!==f?(a=j.jsx(c("PolarisMobilePostCaption.next.react"),{queryReference:f}),e[12]=f,e[13]=a):a=e[13];var t;e[14]!==p||e[15]!==f||e[16]!==g?(t=p&&j.jsx(c("PolarisPostFastViewAllComments.next.react"),{fragmentKey:f,onViewAllCommentsClick:g}),e[14]=p,e[15]=f,e[16]=g,e[17]=t):t=e[17];e[18]!==t?(p=j.jsx(c("IGDSBox.react"),{marginBottom:1,children:t}),e[18]=t,e[19]=p):p=e[19];e[20]!==f?(g=j.jsx(c("PolarisMobilePostPreviewComments.next.react"),{queryReference:f}),e[20]=f,e[21]=g):g=e[21];e[22]!==o||e[23]!==f?(t=!isNaN(o)&&j.jsx(c("IGDSBox.react"),{alignItems:"center",direction:"row",marginTop:1,children:j.jsx(c("PolarisPostTimestamp.react"),{code:f.code,postedAt:o})}),e[22]=o,e[23]=f,e[24]=t):t=e[24];e[25]!==s||e[26]!==a||e[27]!==p||e[28]!==g||e[29]!==t?(o=j.jsxs("div",{className:r,children:[s,a,p,g,t]}),e[25]=s,e[26]=a,e[27]=p,e[28]=g,e[29]=t,e[30]=o):o=e[30];e[31]!==q||e[32]!==o?(r=j.jsxs("div",{children:[q,o]}),e[31]=q,e[32]=o,e[33]=r):r=e[33];return r}g["default"]=a}),98);
__d("PolarisPostHeaderLegacyContainer.next.react",["invariant","CometRelay","IGDSConstants","PolarisMediaConstants","PolarisPostFastOptionsButton.next.react","PolarisPostHeader.react","PolarisPostHeaderFavoritedIconButton.next.react","PolarisPostHeaderLegacyContainer_ad.graphql","PolarisPostHeaderLegacyContainer_media.graphql","PolarisReactRedux","polarisPostSelectors","polarisUserSelectors","react","usePolarisViewer"],(function(a,b,c,d,e,f,g,h){"use strict";var i,j,k,l=(k||(k=d("react"))).unstable_useMemoCache,m=k,n={optionsButton:{display:"x78zum5",justifyContent:"xl56j7k",paddingEnd:"x1ejlxp5",paddingLeft:null,paddingRight:null,$$css:!0},root:{alignItems:"x6s0dn4",display:"x78zum5",flexDirection:"x1q0g3np",$$css:!0}};function a(a){var e,f=l(34),g=a.ad$key;a=a.media$key;a=d("CometRelay").useFragment(i!==void 0?i:i=b("PolarisPostHeaderLegacyContainer_media.graphql"),a);var k=a.affiliate_info,o=a.is_paid_partnership,p=a.media_type,q=a.owner,r=a.pk;g=d("CometRelay").useFragment(j!==void 0?j:j=b("PolarisPostHeaderLegacyContainer_ad.graphql"),g);var s;f[0]!==r?(s=function(a){return d("polarisPostSelectors").getPostById(a,r)},f[0]=r,f[1]=s):s=f[1];var t=d("PolarisReactRedux").useSelector(s);s=d("PolarisReactRedux").useSelector(function(a){return d("polarisPostSelectors").maybeGetOwnerByPost(a,t)});s!=null||h(0,67416);var u;f[2]!==q.pk?(u=function(a){return d("polarisUserSelectors").getUserById(a,q.pk)},f[2]=q.pk,f[3]=u):u=f[3];u=d("PolarisReactRedux").useSelector(u);var v=c("usePolarisViewer")();v=(v==null?void 0:v.id)===s.id;var w;f[4]===Symbol["for"]("react.memo_cache_sentinel")?(w="x6s0dn4 x78zum5 x1q0g3np",f[4]=w):w=f[4];var x;f[5]!==g?(x=g==null?void 0:g.ad_title,f[5]=g,f[6]=x):x=f[6];var y;f[7]!==g?(y=g==null?void 0:g.display_fb_page_name,f[7]=g,f[8]=y):y=f[8];k=(k==null?void 0:k.disclosure_tag)!=null;e=((e=q.group_metadata)==null?void 0:e.is_group)===!0;o=o===!0;var z=t.audience==="MediaAudience.BESTIES";p=p===d("PolarisMediaConstants").MediaTypes.VIDEO;v=!v;var A;f[9]!==x||f[10]!==t.clipsAttributionInfo||f[11]!==t.clipsMusicAttributionInfo||f[12]!==t.location||f[13]!==t.sponsors||f[14]!==y||f[15]!==k||f[16]!==e||f[17]!==o||f[18]!==z||f[19]!==p||f[20]!==r||f[21]!==s||f[22]!==u||f[23]!==v?(A=m.jsx(c("PolarisPostHeader.react"),{adTitle:x,analyticsContext:"postPage",clipsAttributionInfo:t.clipsAttributionInfo,clipsAudioAttributionInfo:t.clipsMusicAttributionInfo,displayFBPageName:y,headerAvatarSize:c("IGDSConstants").AVATAR_SIZES.small,inModal:!1,isAffiliate:k,isOwnerGroupProfile:e,isPaidPartnership:o,isSharedToCloseFriends:z,isSponsored:!1,isVideo:p,location:t.location,mediaId:r,owner:s,postAuthor:u,shouldShowFollowButton:v,showVerifiedBadge:!0,sidebarVariantOptionsButton:!0,sponsors:t.sponsors}),f[9]=x,f[10]=t.clipsAttributionInfo,f[11]=t.clipsMusicAttributionInfo,f[12]=t.location,f[13]=t.sponsors,f[14]=y,f[15]=k,f[16]=e,f[17]=o,f[18]=z,f[19]=p,f[20]=r,f[21]=s,f[22]=u,f[23]=v,f[24]=A):A=f[24];f[25]!==a?(x=m.jsx(c("PolarisPostHeaderFavoritedIconButton.next.react"),{fragmentKey:a}),f[25]=a,f[26]=x):x=f[26];f[27]!==g||f[28]!==a?(y=m.jsx(c("PolarisPostFastOptionsButton.next.react"),{adFragmentKey:g,isOverMedia:!1,mediaKey:a,xstyle:n.optionsButton}),f[27]=g,f[28]=a,f[29]=y):y=f[29];f[30]!==A||f[31]!==x||f[32]!==y?(k=m.jsxs("div",{className:w,children:[A,x,y]}),f[30]=A,f[31]=x,f[32]=y,f[33]=k):k=f[33];return k}g["default"]=a}),98);
__d("usePolarisMediaInitialCarouselIndex",["CometRelay","react","usePolarisMediaInitialCarouselIndex.graphql"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=(i||d("react")).unstable_useMemoCache;function a(a){var c=j(2),e=d("CometRelay").useFragment(h!==void 0?h:h=b("usePolarisMediaInitialCarouselIndex.graphql"),a);if(c[0]!==e){a=(a=e.carousel_media)==null?void 0:a.findIndex(function(a){a=a.pk;return a===e.main_feed_carousel_starting_media_id});c[0]=e;c[1]=a}else a=c[1];c=a;return c==null||c===-1?0:c}g["default"]=a}),98);
__d("usePolarisPostViewpointLogging",["CometRelay","PolarisOrganicImpressionAction.next","PolarisViewpointReact.react","PolarisVpvdImpressionAction.next","usePolarisPostViewpointLogging.graphql"],(function(a,b,c,d,e,f,g){"use strict";var h;function a(a,c){a=d("CometRelay").useFragment(h!==void 0?h:h=b("usePolarisPostViewpointLogging.graphql"),a);return d("PolarisViewpointReact.react").useViewpoint({action:[d("PolarisOrganicImpressionAction.next").usePostImpressionAction(a,c),d("PolarisVpvdImpressionAction.next").usePostVpvdImpressionAction(a,c)],id:a.pk})}g["default"]=a}),98);
__d("PolarisMobilePost.next.react",["CometRelay","CometRouteParams","PolarisMedia.next.react","PolarisMobilePostDetailsSection.next.react","PolarisMobilePostFragment.graphql","PolarisPostContext.react","PolarisPostHeaderLegacyContainer.next.react","PolarisPostSidecarIndexHelpers","react","usePolarisMediaInitialCarouselIndex","usePolarisPostSetURLSidecarIndex","usePolarisPostViewpointLogging"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=i||(i=d("react"));e=i;e.useCallback;var k=e.useState,l=e.unstable_useMemoCache,m=function(a,b){if(!d("PolarisPostSidecarIndexHelpers").shouldHaveIndexableUrls()||a==null)return b;a=parseInt(a,10)-1;return a<0?b:a};function a(a){var e=l(20);a=a.queryReference;a=d("CometRelay").useFragment(h!==void 0?h:h=b("PolarisMobilePostFragment.graphql"),a);var f=c("usePolarisMediaInitialCarouselIndex")(a),g=c("usePolarisPostViewpointLogging")(a,"postPage"),i=d("CometRouteParams").useRouteParams();i=i.img_index;i=k(m(i,f));f=i[0];var n=i[1],o=c("usePolarisPostSetURLSidecarIndex")();e[0]!==o?(i=function(a,b,c){n(b),d("PolarisPostSidecarIndexHelpers").shouldHaveIndexableUrls()&&o(b+1)},e[0]=o,e[1]=i):i=e[1];i=i;var p;e[2]===Symbol["for"]("react.memo_cache_sentinel")?(p="x78zum5 xdt5ytf",e[2]=p):p=e[2];var q;e[3]!==a?(q=j.jsx(c("PolarisPostHeaderLegacyContainer.next.react"),{media$key:a}),e[3]=a,e[4]=q):q=e[4];var r;e[5]!==i||e[6]!==f||e[7]!==a?(r=j.jsx(c("PolarisMedia.next.react"),{analyticsContext:"postPage",handleMediaSidecarChildIndexChange:i,initialCarouselIndex:f,mediaFragmentKey:a}),e[5]=i,e[6]=f,e[7]=a,e[8]=r):r=e[8];e[9]!==a?(i=j.jsx(c("PolarisMobilePostDetailsSection.next.react"),{queryReference:a}),e[9]=a,e[10]=i):i=e[10];var s;e[11]!==f||e[12]!==a||e[13]!==q||e[14]!==r||e[15]!==i?(s=j.jsxs(d("PolarisPostContext.react").PolarisPostContextProvider,{analyticsContext:"postPage",currentSidecarIndex:f,queryReference:a,children:[q,r,i]}),e[11]=f,e[12]=a,e[13]=q,e[14]=r,e[15]=i,e[16]=s):s=e[16];e[17]!==g||e[18]!==s?(f=j.jsx("div",{className:p,"data-testid":void 0,ref:g,children:s}),e[17]=g,e[18]=s,e[19]=f):f=e[19];return f}g["default"]=a}),98);
__d("PolarisDesktopPostRoot.react",["CometPlaceholder.react","IGDSBox.react","IGDSSpinner.react","deferredLoadComponent","react","requireDeferredForDisplay","withPolarisShell"],(function(a,b,c,d,e,f,g){"use strict";var h,i=(h||(h=d("react"))).unstable_useMemoCache,j=h,k=c("deferredLoadComponent")(c("requireDeferredForDisplay")("PolarisDesktopPostPage.next.react").__setRef("PolarisDesktopPostRoot.react"));function a(a){var b=i(4),d=a.props;a=a.queries;d=d.routeProps;d=d.media_id;var e;b[0]===Symbol["for"]("react.memo_cache_sentinel")?(e=j.jsx(c("IGDSBox.react"),{alignItems:"center",display:"flex",flex:"grow",height:"100%",justifyContent:"center",width:"100%",children:j.jsx(c("IGDSSpinner.react"),{})}),b[0]=e):e=b[0];b[1]!==d||b[2]!==a?(e=j.jsx(c("CometPlaceholder.react"),{fallback:e,children:j.jsx(k,{postId:d,queries:a})}),b[1]=d,b[2]=a,b[3]=e):e=b[3];return e}b=c("withPolarisShell")(a);g["default"]=b}),98);
__d("PolarisMobileChainedPosts.next.react",["invariant","CometRelay","PolarisChainedPostsPaginationQuery","PolarisErrorBoundary.react","PolarisGenericVirtualFeed.react","PolarisMediaChainingPageConstants","PolarisMobilePost.next.react","emptyFunction","react","useCurrentRoute"],(function(a,b,c,d,e,f,g,h){"use strict";var i,j=i||(i=d("react"));b=i;b.useCallback;var k=b.unstable_useMemoCache;function a(a){var b=k(15);a=a.queryReference;a=d("CometRelay").usePaginationFragment(c("PolarisChainedPostsPaginationQuery"),a);var e=a.data,f=a.isLoadingNext,g=a.loadNext;b[0]!==e.xdt_api__v1__discover__chaining_experience_feed_connection.edges?(a=e.xdt_api__v1__discover__chaining_experience_feed_connection.edges.map(function(a){return a.node.media_or_ad}),b[0]=e.xdt_api__v1__discover__chaining_experience_feed_connection.edges,b[1]=a):a=b[1];var i=a;e=c("useCurrentRoute")();if(b[2]!==e){a=e==null?void 0:(a=e.rootView.props)==null?void 0:a.media_id;b[2]=e;b[3]=a}else a=b[3];var l=a;l!=null||h(0,68702);b[4]!==g||b[5]!==l||b[6]!==i.length?(e=function(){g(10,{UNSTABLE_extraVariables:{data:{media_id:l,num_total_items:i.length}}})},b[4]=g,b[5]=l,b[6]=i.length,b[7]=e):e=b[7];a=e;b[8]!==i?(e=function(a){a=a.index;return i[a]==null?null:j.jsx(c("PolarisErrorBoundary.react"),{errorRenderer:c("emptyFunction").thatReturnsNull,children:j.jsx(c("PolarisMobilePost.next.react"),{queryReference:i[a]})},a)},b[8]=i,b[9]=e):e=b[9];e=e;var m;b[10]!==f||b[11]!==i||b[12]!==a||b[13]!==e?(m=j.jsx(c("PolarisGenericVirtualFeed.react"),{allowSampledScrollLogging:!1,analyticsContext:d("PolarisMediaChainingPageConstants").MEDIA_CHAINING_ANALYTICS_CONTEXT,enablePrefetch:!1,enablePriorityFetching:!0,hasNextPage:!0,isFetching:f,items:i,onNextPage:a,renderFeedItem:e,visibleCount:i.length}),b[10]=f,b[11]=i,b[12]=a,b[13]=e,b[14]=m):m=b[14];return m}g["default"]=a}),98);
__d("PolarisMobileChainedPostsContainer.next.react",["CometRelay","PolarisChainedPostsRootQuery","PolarisMobileChainedPosts.next.react","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i=(h||(h=d("react"))).unstable_useMemoCache,j=h;function a(a){var b=i(2);a=a.polarisPostChainingRootQuery;a=d("CometRelay").usePreloadedQuery(c("PolarisChainedPostsRootQuery"),a);var e;b[0]!==a?(e=j.jsx(c("PolarisMobileChainedPosts.next.react"),{queryReference:a}),b[0]=a,b[1]=e):e=b[1];return e}g["default"]=a}),98);
__d("PolarisPostPageMetadata.next.react",["CometRelay","PolarisMonitorErrors","PolarisPageMetadata.react","PolarisPostPageMetadataFragment.graphql","err","getPolarisTitleForPost","polarisGetPostFromGraphMediaInterface","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=(i||(i=d("react"))).unstable_useMemoCache,k=i;function a(a){var e=j(10),f=a.pageIdentifier;a=a.queryReference;a=d("CometRelay").useFragment(h!==void 0?h:h=b("PolarisPostPageMetadataFragment.graphql"),a);var g=a.caption,i=a.media_type,l=a.owner,m=a.product_type,n=a.taken_at;a=a.title;if(l==null){d("PolarisMonitorErrors").logError(c("err")("Post owner was unexpectedly null"));return null}var o;e[0]!==m||e[1]!==a||e[2]!==g||e[3]!==i||e[4]!==n||e[5]!==l?(o=d("polarisGetPostFromGraphMediaInterface").isClipsProductType(m)&&a!=null&&a.trim()!==""?a:c("getPolarisTitleForPost")({caption:g==null?void 0:g.text,isVideo:i===2,postedAt:Number(n)},{fullName:l.full_name,username:l.username}),e[0]=m,e[1]=a,e[2]=g,e[3]=i,e[4]=n,e[5]=l,e[6]=o):o=e[6];m=o;e[7]!==f||e[8]!==m?(a=k.jsx(c("PolarisPageMetadata.react"),{base:"",id:f,title:m}),e[7]=f,e[8]=m,e[9]=a):a=e[9];return a}g["default"]=a}),98);
__d("PolarisPostPageWrapper.react",["CometRelay","IGDSDialogBackwardsCompatibilityWrapper.react","PolarisBoostHandleCreationFlow.react","PolarisEntityQRModalLazy.react","PolarisPostPageMetadata.next.react","PolarisPostPageWrapperFragment.graphql","react","useCurrentRoute"],(function(a,b,c,d,e,f,g){"use strict";var h,i,j=i||(i=d("react"));e=i;var k=e.useState,l=e.unstable_useMemoCache;function a(a){var e=l(10),f=a.children;a=a.queryReference;a=d("CometRelay").useFragment(h!==void 0?h:h=b("PolarisPostPageWrapperFragment.graphql"),a);var g=c("useCurrentRoute")();g=k((g==null?void 0:(g=g.rootView.props)==null?void 0:g.qr)===!0);var i=g[0],m=g[1];e[0]!==a?(g=j.jsx(c("PolarisPostPageMetadata.next.react"),{pageIdentifier:"postPage",queryReference:a}),e[0]=a,e[1]=g):g=e[1];var n;e[2]===Symbol["for"]("react.memo_cache_sentinel")?(n=j.jsx(c("PolarisBoostHandleCreationFlow.react"),{}),e[2]=n):n=e[2];var o;e[3]!==i||e[4]!==a?(o=i===!0&&j.jsx(c("IGDSDialogBackwardsCompatibilityWrapper.react"),{children:j.jsx(c("PolarisEntityQRModalLazy.react"),{entityID:a.pk,onClose:function(){return m(!1)},source:"DIRECT_NAVIGATION"})}),e[3]=i,e[4]=a,e[5]=o):o=e[5];e[6]!==g||e[7]!==f||e[8]!==o?(i=j.jsxs(j.Fragment,{children:[g,n,f,o]}),e[6]=g,e[7]=f,e[8]=o,e[9]=i):i=e[9];return i}g["default"]=a}),98);
__d("PolarisMobilePostPage.next.react",["CometRelay","ErrorBoundary.react","FBLogger","PolarisMobilePost.next.react","PolarisPostPageGatedContentAPIReasonFallback.react","PolarisPostPageWrapper.react","PolarisPostRootQuery.graphql","react"],(function(a,b,c,d,e,f,g){"use strict";var h,i=h||(h=d("react"));b=h;b.useCallback;var j=b.unstable_useMemoCache;function k(a){var b=j(8);a=a.polarisPostRootQuery;a=d("CometRelay").usePreloadedQuery(c("PolarisPostRootQuery.graphql"),a);if(b[0]!==a.xdt_api__v1__media__shortcode__web_info.items){var e;e=(e=a.xdt_api__v1__media__shortcode__web_info.items)==null?void 0:e[0];b[0]=a.xdt_api__v1__media__shortcode__web_info.items;b[1]=e}else e=b[1];a=e;if(a==null)throw c("FBLogger")("ig_web").mustfixThrow("Post page item does not exist");b[2]===Symbol["for"]("react.memo_cache_sentinel")?(e="xh8yej3",b[2]=e):e=b[2];b[3]!==a?(e=i.jsx("div",{className:e,"data-testid":void 0,children:i.jsx(c("PolarisMobilePost.next.react"),{queryReference:a})}),b[3]=a,b[4]=e):e=b[4];var f;b[5]!==a||b[6]!==e?(f=i.jsx(c("PolarisPostPageWrapper.react"),{queryReference:a,children:e}),b[5]=a,b[6]=e,b[7]=f):f=b[7];return f}function a(a){var b=j(7),d;b[0]!==a.postId?(d=function(b){return i.jsx(c("PolarisPostPageGatedContentAPIReasonFallback.react"),{error:b,fullpage:!1,postId:a.postId})},b[0]=a.postId,b[1]=d):d=b[1];d=d;var e;b[2]!==a?(e=i.jsx(k,babelHelpers["extends"]({},a)),b[2]=a,b[3]=e):e=b[3];var f;b[4]!==d||b[5]!==e?(f=i.jsx(c("ErrorBoundary.react"),{fallback:d,children:e}),b[4]=d,b[5]=e,b[6]=f):f=b[6];return f}g["default"]=a}),98);
__d("PolarisMobilePostPageHeader.next.react",["fbt","PolarisGenericMobileHeader.react","PolarisNavBackButton.react","PolarisShellMobileHeader.react","react","usePolarisViewer"],(function(a,b,c,d,e,f,g,h){"use strict";var i,j=(i||(i=d("react"))).unstable_useMemoCache,k=i,l=h._("__JHASH__tsG71JEKkVB__JHASH__");function a(){var a=j(4),b=c("usePolarisViewer")(),d;a[0]===Symbol["for"]("react.memo_cache_sentinel")?(d=[k.jsx(c("PolarisNavBackButton.react"),{analyticsContext:"postPage"},"back")],a[0]=d):d=a[0];d=d;a[1]===Symbol["for"]("react.memo_cache_sentinel")?(d=k.jsx(c("PolarisGenericMobileHeader.react"),{leftActions:d,title:l}),a[1]=d):d=a[1];d=d;a[2]!==b?(d=k.jsx(c("PolarisShellMobileHeader.react"),{mobileHeader:d,viewer:b}),a[2]=b,a[3]=d):d=a[3];return d}g["default"]=a}),98);
__d("PolarisMobilePostRoot.react",["CometPlaceholder.react","IGDSBox.react","PolarisMobilePostPageHeader.next.react","PolarisMorePostsLikeThisHeader.react","PolarisPostGlimmer.react","deferredLoadComponent","qex","react","requireDeferredForDisplay","useRouteReferrer","withPolarisShell"],(function(a,b,c,d,e,f,g){"use strict";var h,i=(h||(h=d("react"))).unstable_useMemoCache,j=h,k=c("deferredLoadComponent")(c("requireDeferredForDisplay")("PolarisMobilePostPage.next.react").__setRef("PolarisMobilePostRoot.react")),l=c("deferredLoadComponent")(c("requireDeferredForDisplay")("PolarisMobileChainedPostsContainer.next.react").__setRef("PolarisMobilePostRoot.react"));function a(a){var b,d=i(9),e=a.props;a=a.queries;var f=c("useRouteReferrer")();f=(f==null?void 0:f.navigationType)==="navigation"&&(f==null?void 0:f.tracePolicy)==="polaris.profilePage";f=!f&&c("qex")._("591")===!0;b=((b=e.routeParams)==null?void 0:b.chaining)===!0||f;d[0]===Symbol["for"]("react.memo_cache_sentinel")?(f=j.jsx(c("PolarisMobilePostPageHeader.next.react"),{}),d[0]=f):f=d[0];var g;d[1]===Symbol["for"]("react.memo_cache_sentinel")?(g=j.jsx(c("PolarisPostGlimmer.react"),{}),d[1]=g):g=d[1];var h;d[2]!==a.polarisPostRootQuery||d[3]!==e.routeProps.media_id?(h=j.jsx(k,{polarisPostRootQuery:a.polarisPostRootQuery,postId:e.routeProps.media_id}),d[2]=a.polarisPostRootQuery,d[3]=e.routeProps.media_id,d[4]=h):h=d[4];d[5]!==h||d[6]!==b||d[7]!==a?(e=j.jsxs(j.Fragment,{children:[f,j.jsx(c("CometPlaceholder.react"),{fallback:g,children:h}),b&&a.polarisPostChainingRootQuery!=null&&j.jsxs(j.Fragment,{children:[j.jsx(c("PolarisMorePostsLikeThisHeader.react"),{}),j.jsx(c("IGDSBox.react"),{marginTop:4,children:j.jsx(c("CometPlaceholder.react"),{fallback:j.jsx(c("PolarisPostGlimmer.react"),{}),children:j.jsx(l,{polarisPostChainingRootQuery:a.polarisPostChainingRootQuery})})})]})]}),d[5]=h,d[6]=b,d[7]=a,d[8]=e):e=d[8];return e}b=c("withPolarisShell")(a);g["default"]=b}),98);