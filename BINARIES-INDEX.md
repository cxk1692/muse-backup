# 二进制文件索引（以 base64 文本形式保存）

这些文件是图片/文档等二进制内容，本仓库里以「原路径 + .b64」存放。恢复时对每个文件执行：

`base64 -d 原路径.b64 > 原路径`

然后用下面的 SHA-256 校验解出的文件是否完整。

| 原文件 | 原大小(字节) | SHA-256 |
|---|---|---|
| projects/goals/goal/briefs/.artifacts/letter-74af562388cd/.space-build-cvm/assets/0.webp | 499566 | 064c0dfcfc1a55dc0c5d72d1cfd5ccf2c1ba1942cb2c4867787cadde7b8d6a38 |
| projects/goals/goal/briefs/.artifacts/letter-74af562388cd/.space-build/assets/0.webp | 499566 | 064c0dfcfc1a55dc0c5d72d1cfd5ccf2c1ba1942cb2c4867787cadde7b8d6a38 |
| projects/goals/goal/briefs/media/media-generation-seven-night-log-hero-0-d96d3438-3465-44a8-8807-81cf564e6367.webp | 499566 | 064c0dfcfc1a55dc0c5d72d1cfd5ccf2c1ba1942cb2c4867787cadde7b8d6a38 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/amplifier.jpg | 120873 | 22aae74c5e713e7284f73e0ea4cdd0ecdc38c449ae2c92a669b10112c717cf22 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/article-01-typeset.docx | 606751 | cef3c08a432eeaea74974ece8f5521d1a4fae36018403ba4b1783aca4fa5683e |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/article-03-typeset.docx | 1614152 | c649e7f34427b4858d5082f46e67a5b447b8790130660f114a0957d57a01d64e |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/article-03-v2-typeset.docx | 1614266 | d8f27ea8d811da0ae7c13d26aaae081634fa52a0fef5a7ccd6769d85f2831943 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/article-03-v3-typeset.docx | 1613478 | 142fe927c2912541be431b3421b9faa7a7ceda067a34f057e3e1b6c5e26c0b58 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-bg-circuit.png | 999235 | 10831dfa4f0b672c53c9a96767d26908cb15e8433ece0f82b40df94690c9d73f |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-bg-network.png | 1106523 | c8237aa67e451f9a6cc5bab04f9b14033191326f5ec663fdd298214f2d721693 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-calligraphy-circuit-light.png | 401497 | fcfe494e3c70ade5f053e7f76c66de97cb6d2168232f41bdc425b59a17c322dc |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-calligraphy-pixel-light.png | 299593 | 654efa31487afd54cb16275764ad5b160d127e924169943a44d4f9669cd31bf0 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-calligraphy.png | 299218 | 14a31c4c9408f1cd4c0c2937188163807e19506709fd8e27d40fb6316dae7d58 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-circuit.png | 408814 | 7d726b877df4dfda5bc77a82b2b1df448b354a56a60a530bbdcfb72b9c68cb26 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-pixel.png | 191595 | d94dee64fc7b4cf83e4f7f9f4cc6775909cd8de255ec419482e17c406a8d9430 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/avatar-songti.png | 57437 | d77f5c0537715c205f6b29afd7b413419653ef8576f527049f4371e3fb754de4 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/circuit.jpg | 141507 | 4524b334a5fb94114b36c668e7c82c53318ca72944919711e7b17d5db9bf4264 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/cover.jpg | 236558 | ea4201c85ec51cfe87075dedf75e1804740a1b6999725765669906aff494e123 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/cover3.jpg | 319090 | 55bead9d78b626c76f3f2794e94609886711714089136137c81828ba34f9df06 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/desk.jpg | 220838 | 12e84163aa848ed15c269c3968627bbb032277a249401044ce421b09332a0a85 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/final.jpg | 111960 | 27734d678ba42b93bd3d4cb923b2f6856b5139e6a85ab067d7776e2c65cbc630 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/neon.jpg | 893071 | c2b6a29bec877e834154127dd24fc1ab68c1060dced5782b84a7657e873f7a11 |
| projects/goals/ordinary-worker-ai-practice-wechat-account/files/kuai-ai-shouji/ppt.jpg | 192441 | e772fff1c0c1c52ca7d0bd2ab7f9106cbaa8f8b56dc5e9adacee986acdbb580d |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/刮大白刷漆全套整理.docx | 39585 | 7f5a317843ee3dc8ab74c2a485348868c8efeb129fa878e4f4c3d5e726f200ad |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/刮大白刷漆包工包料合同-最新版.docx | 38763 | 09fdc8d0641d3f3dff72040ebf3cc1084d2888a520f3e62aea8eaddfa30a287b |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/刮大白刷漆包工包料合同-最终版.docx | 39169 | db8b8d7b38e7bca7c4ce1685ec9f9f953528fc6efccf8ea11ac639d24e7680a6 |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/刮大白刷漆包工包料合同-最终版.pdf | 177407 | ed9fad0f98de244fe9040e24a3e807cfeba4d8ef3804d941aecd179adf7282ca |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/刮大白刷漆包工包料简易合同.docx | 39875 | 81c8092fe9d073c12d827edcf2a3c183b7d09527972837803dd70f32c29b8077 |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/刮大白刷漆包工包料简易合同.pdf | 201281 | 4a3e3d13285def00e44f7a05592c639123dc1332015108d20a0ff17cdbff8ed7 |
| projects/goals/self-built-home-wall-putty-renovation/files/gua-dabai-contract/自建房刮大白承包合同-刮三遍版.docx | 41787 | 7ea28a40dceae711a7889f2d1d5c784c51c58e4d8c021416183b0417680f3fae |
| projects/goals/vpn/hidden_files/hy2-qr.png | 598 | 95053dc805caa78f9c0343e650dbbcc459b213d12c8ffadec7f59d89f35fdc4d |
| projects/your_files/oracle-ticket-cover-v2.png | 90293 | 9b341c9047d730c2fcd9bfe9a7f319fbc78eb859f973f221d1f009685917461e |
| projects/your_files/oracle-ticket-cover-v3.png | 758483 | f3fcdddef801bf0996e045832156ba46bcc947e4f3393f52b2531aeba4fd83fb |
| projects/your_files/oracle-ticket-cover.png | 62213 | 2bda602e9bfac994e1dc2192c378be5d5be8d7f80f85e6b8671e0308e363f6f6 |
| projects/your_files/voice-message.mp3 | 115621 | 0b9804a1cda998507cb729681373844f205f356656d4c247ea750b77c742ed6f |
