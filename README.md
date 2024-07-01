# About
Script which uses **pyautogui** to manually draw an image in MS Paint

## Examples
(bad timelapse)

![Recording2024-06-10144147-ezgif com-video-to-gif-converter](https://github.com/aiden10/paint/assets/51337166/f21babc4-1554-46cd-81f7-78ee2d9655c5)

![ghibli](https://github.com/aiden10/paint/assets/51337166/f89e5163-2a27-401c-bfc9-4b041e073e53)
![melon](https://github.com/aiden10/paint/assets/51337166/e463b8fa-f2de-4285-85e4-72fc2b05ef41)
![portal](https://github.com/aiden10/paint/assets/51337166/b273e532-4f42-4796-9548-cc120cd07567)

## Notes
The 'step' parameter can be adjusted to speed up the process at the cost of worse quality (step is just the increment while iterating over the pixels). And the reduce_colors function outputs and image with a limited color palette (specified by the parameter). Less colors means less time is spent changing colors which means faster drawing. Lastly, if you do for some reason want to use this, all you need to do is update the coordinates of the canvas edges. The coordinates can be gotten easily with `pyautogui.mouseInfo()`.
- ### Original Image (limited to 48 colors)
  ![reduced_minecraft](https://github.com/aiden10/paint/assets/51337166/945fd6b6-adef-48b1-aa71-615b7b0a21ba)
- ### 20 Step
  ![minecraft20step](https://github.com/aiden10/paint/assets/51337166/8bf0469c-bf1a-4944-9c62-ddb358abb348)
- ### 10 Step
  ![minecraft10step](https://github.com/aiden10/paint/assets/51337166/2732048f-eb1c-429f-aed1-7b32b40f2c20)
- ### 5 Step
  ![minecraft5step](https://github.com/aiden10/paint/assets/51337166/d536bc54-b8a9-48b2-8856-c72f3388f44f)
- ### 2 Step
  ![minecraft2step](https://github.com/aiden10/paint/assets/51337166/a9615565-6eda-4cc6-957c-bf8b8188b2ba)
