// // chrome.tabs.onActivated.addListener(
// //     () => {
// //         chrome.tabs.query({"active": true},
// //             function(tab) {
// //                 try {
// //                     console.log('Current tab URL is: ', tab[0]);
// //                     console.log('Current tab URL is: ', tab[0]["url"]);
// //                 } catch (e) {
// //                     console.log(e);
// //                 }
// //             }
// //         )
// //     }
// // )  


// // import { video_id } from './script.js';
// // import { extractVideoId } from './script.js';

// // Extract video id
// function extractVideoId(url) {
//     // Split the URL string at 'v=' and return the last part
//     const parts = url.split('v=');
//     console.log(parts);
//     if (parts.length > 1) {
//         let video_id = parts[1];
//         chrome.storage.local.set({ "video_id": video_id }).then(() => { console.log("Value is set"); });
//     } else {
//         console.error('Invalid YouTube URL');
//         return null;
//     }
// }

// chrome.tabs.onActivated.addListener(() => {
//     chrome.tabs.query({ "active": true }, function (tab) {
//         try {
//             const video_url = tab[0]["url"];
//             const video_id = extractVideoId(video_url);
//         } catch (e) {
//             console.log(e);
//         }
//     });
// });