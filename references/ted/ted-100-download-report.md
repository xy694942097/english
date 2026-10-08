# TED 100 篇英文字幕下载清单

2026-10-08：成功 **100/100**；保存 100 份官方英文 JSON 原件，并生成 100 份 SRT，共 **31,107 条字幕**，合计 **5.74 MiB**。未下载视频或音频。

本地目录：`materials/corpus/ted/english/`。文件名为 `目录编号-TED ID.en.json` 与 `.en.srt`；编号与 [100 篇选材目录](ted-100-catalog.md) 一致。JSON 是接口原始字节，SRT 使用每条原始 `startTime` 和 `duration` 生成，没有用下一条开始时间猜结束时间。

已逐文件复验字节数与 SHA-256，核对字幕非空、编号连续、时间不倒退、持续时长为正、99 份的覆盖范围与目录时长相符；084 有官方源时长差异，详见下文。API 时间轴可能不含播放器片头，尚未逐条听校或保证与用户的视频版本同步。

[下载结果与哈希](ted-100-download-results.json) · [资料 manifest](../../materials/downloads-manifest.json) · [官方字幕与文本说明](https://help.ted.com/hc/en-us/articles/360018572954-How-do-I-find-transcripts-for-TED-and-TEDx-talks)

## 文件索引

| 编号 | 演讲 | SRT 文件 | 字幕条数 | 覆盖至 |
|---|---|---|---:|---:|
| 001 | [拖延症患者的大脑](https://www.ted.com/talks/tim_urban_inside_the_mind_of_a_master_procrastinator) | `001-2458.en.srt` | 315 | 0:13:50 |
| 002 | [怎样说话，别人才愿意听](https://www.ted.com/talks/julian_treasure_how_to_speak_so_that_people_want_to_listen) | `002-2034.en.srt` | 229 | 0:09:39 |
| 003 | [学校扼杀创造力吗？](https://www.ted.com/talks/sir_ken_robinson_do_schools_kill_creativity) | `003-66.en.srt` | 427 | 0:19:00 |
| 004 | [脆弱的力量](https://www.ted.com/talks/brene_brown_the_power_of_vulnerability) | `004-1042.en.srt` | 391 | 0:19:58 |
| 005 | [什么造就美好生活？最长幸福研究的启示](https://www.ted.com/talks/robert_waldinger_what_makes_a_good_life_lessons_from_the_longest_study_on_happiness) | `005-2399.en.srt` | 212 | 0:12:33 |
| 006 | [回复垃圾邮件会发生什么？](https://www.ted.com/talks/james_veitch_this_is_what_happens_when_you_reply_to_spam_email) | `006-2405.en.srt` | 208 | 0:09:35 |
| 007 | [AI 如何回答我们尚未想到的问题](https://www.ted.com/talks/aravind_srinivas_how_ai_will_answer_questions_we_haven_t_thought_to_ask) | `007-144591.en.srt` | 217 | 0:11:31 |
| 008 | [认识机器人管家 NEO](https://www.ted.com/talks/bernt_bornich_meet_neo_your_robot_butler_in_training) | `008-148292.en.srt` | 275 | 0:14:44 |
| 009 | [下一台电脑是你的眼镜？](https://www.ted.com/talks/shahram_izadi_the_next_computer_your_glasses) | `009-148309.en.srt` | 338 | 0:16:03 |
| 010 | [AI 革命被低估了](https://www.ted.com/talks/eric_schmidt_the_ai_revolution_is_underhyped) | `010-148366.en.srt` | 577 | 0:25:33 |
| 011 | [让对话更好的十种方法](https://www.ted.com/talks/celeste_headlee_10_ways_to_have_a_better_conversation) | `011-2435.en.srt` | 247 | 0:11:16 |
| 012 | [访谈的艺术](https://www.ted.com/talks/marc_pachter_the_art_of_the_interview) | `012-708.en.srt` | 400 | 0:20:34 |
| 013 | [连接着，却孤独着？](https://www.ted.com/talks/sherry_turkle_connected_but_alone) | `013-1409.en.srt` | 461 | 0:19:27 |
| 014 | [沉默的危险](https://www.ted.com/talks/clint_smith_the_danger_of_silence) | `014-2059.en.srt` | 101 | 0:04:04 |
| 015 | [邀请“另一方”共进午餐](https://www.ted.com/talks/elizabeth_lesser_take_the_other_to_lunch) | `015-1052.en.srt` | 186 | 0:10:47 |
| 016 | [你是人类吗？](https://www.ted.com/talks/ze_frank_are_you_human) | `016-2049.en.srt` | 87 | 0:04:16 |
| 017 | [婴儿在想什么？](https://www.ted.com/talks/alison_gopnik_what_do_babies_think) | `017-1241.en.srt` | 429 | 0:18:08 |
| 018 | [把废物变成学习玩具](https://www.ted.com/talks/arvind_gupta_turning_trash_into_toys_for_learning) | `018-1135.en.srt` | 367 | 0:15:09 |
| 019 | [建立一所云端学校](https://www.ted.com/talks/sugata_mitra_build_a_school_in_the_cloud) | `019-1678.en.srt` | 419 | 0:22:09 |
| 020 | [坚毅：热情与坚持的力量](https://www.ted.com/talks/angela_lee_duckworth_grit_the_power_of_passion_and_perseverance) | `020-1733.en.srt` | 116 | 0:05:54 |
| 021 | [一个坚持要上学的女孩](https://www.ted.com/talks/kakenya_ntaiya_a_girl_who_demanded_school) | `021-1672.en.srt` | 277 | 0:14:54 |
| 022 | [把艺术与科学一起教](https://www.ted.com/talks/mae_jemison_teach_arts_and_sciences_together) | `022-533.en.srt` | 462 | 0:21:03 |
| 023 | [一次教好一个孩子](https://www.ted.com/talks/shukla_bose_teaching_one_child_at_a_time) | `023-809.en.srt` | 318 | 0:16:02 |
| 024 | [献给受欺凌者与美丽的人](https://www.ted.com/talks/shane_koyczan_to_this_day_for_the_bullied_and_beautiful) | `024-1687.en.srt` | 243 | 0:11:34 |
| 025 | [贫民区里的教育创新](https://www.ted.com/talks/charles_leadbeater_education_innovation_in_the_slums) | `025-892.en.srt` | 472 | 0:18:35 |
| 026 | [用视频重新构想教育](https://www.ted.com/talks/sal_khan_let_s_use_video_to_reinvent_education) | `026-1090.en.srt` | 438 | 0:20:05 |
| 027 | [为什么发泄不能帮你处理愤怒](https://www.ted.com/talks/jennifer_parlamis_why_venting_doesn_t_help_you_deal_with_anger) | `027-158796.en.srt` | 309 | 0:14:58 |
| 028 | [抑郁症为什么不是你想的那样](https://www.ted.com/talks/lisa_monteggia_why_depression_isn_t_what_you_think) | `028-184094.en.srt` | 273 | 0:13:07 |
| 029 | [我教老鼠开车，它们教我享受过程](https://www.ted.com/talks/kelly_lambert_i_taught_rats_to_drive_they_taught_me_to_enjoy_the_ride) | `029-174584.en.srt` | 290 | 0:13:56 |
| 030 | [压力重置：心理健康的一种工具](https://www.ted.com/talks/jenny_taitz_stress_resets_the_ultimate_mental_health_hack) | `030-175298.en.srt` | 209 | 0:10:26 |
| 031 | [怎样过有意义的生活](https://www.ted.com/talks/brian_s_lowery_how_to_live_a_meaningful_life) | `031-136666.en.srt` | 279 | 0:13:58 |
| 032 | [幸福生活的秘密：八十年研究的启示](https://www.ted.com/talks/robert_waldinger_the_secret_to_a_happy_life_lessons_from_8_decades_of_research) | `032-102335.en.srt` | 508 | 0:28:34 |
| 033 | [抑郁时怎样洗衣服](https://www.ted.com/talks/kc_davis_how_to_do_laundry_when_you_re_depressed_sep_2022) | `033-102438.en.srt` | 259 | 0:12:53 |
| 034 | [自我感从哪里来？一个科学视角](https://www.ted.com/talks/anil_ananthaswamy_where_does_your_sense_of_self_come_from_a_scientific_look) | `034-102332.en.srt` | 229 | 0:12:27 |
| 035 | [你并非任由情绪摆布：大脑创造情绪](https://www.ted.com/talks/lisa_feldman_barrett_you_aren_t_at_the_mercy_of_your_emotions_your_brain_creates_them) | `035-8419.en.srt` | 332 | 0:18:15 |
| 036 | [怎样修复破碎的心](https://www.ted.com/talks/guy_winch_how_to_fix_a_broken_heart) | `036-9987.en.srt` | 241 | 0:12:09 |
| 037 | [幸福的意外科学](https://www.ted.com/talks/dan_gilbert_the_surprising_science_of_happiness) | `037-97.en.srt` | 452 | 0:20:46 |
| 038 | [选择、幸福与意大利面酱](https://www.ted.com/talks/malcolm_gladwell_choice_happiness_and_spaghetti_sauce) | `038-20.en.srt` | 381 | 0:17:12 |
| 039 | [幸福及其意外之处](https://www.ted.com/talks/nancy_etcoff_happiness_and_its_surprises) | `039-570.en.srt` | 342 | 0:14:01 |
| 040 | [心流：幸福的秘密](https://www.ted.com/talks/mihaly_csikszentmihalyi_flow_the_secret_to_happiness) | `040-366.en.srt` | 256 | 0:18:38 |
| 041 | [怎样用钱买到幸福](https://www.ted.com/talks/michael_norton_how_to_buy_happiness) | `041-1427.en.srt` | 263 | 0:10:38 |
| 042 | [选择的悖论](https://www.ted.com/talks/barry_schwartz_the_paradox_of_choice) | `042-93.en.srt` | 412 | 0:19:18 |
| 043 | [想幸福？学会感恩](https://www.ted.com/talks/david_steindl_rast_want_to_be_happy_be_grateful) | `043-1880.en.srt` | 243 | 0:14:08 |
| 044 | [记得说谢谢](https://www.ted.com/talks/laura_trice_remember_to_say_thank_you) | `044-349.en.srt` | 80 | 0:03:11 |
| 045 | [更少物品，更多幸福](https://www.ted.com/talks/graham_hill_less_stuff_more_happiness) | `045-1238.en.srt` | 132 | 0:05:28 |
| 046 | [幸福的习惯](https://www.ted.com/talks/matthieu_ricard_the_habits_of_happiness) | `046-191.en.srt` | 352 | 0:20:37 |
| 047 | [在任何年龄发现真实的自己](https://www.ted.com/talks/bevy_smith_how_to_discover_your_authentic_self_at_any_age) | `047-91710.en.srt` | 355 | 0:15:05 |
| 048 | [每周工作四天的理由](https://www.ted.com/talks/juliet_schor_the_case_for_a_4_day_work_week) | `048-92266.en.srt` | 207 | 0:11:37 |
| 049 | [优秀领导为何认真对待幽默](https://www.ted.com/talks/jennifer_aaker_and_naomi_bagdonas_why_great_leaders_take_humor_seriously) | `049-83756.en.srt` | 209 | 0:09:06 |
| 050 | [职场中过于“好说话”的问题](https://www.ted.com/talks/tessa_west_the_problem_with_being_too_nice_at_work_sep_2024) | `050-131384.en.srt` | 404 | 0:16:51 |
| 051 | [善意在工作中的价值](https://www.ted.com/talks/james_rhee_the_value_of_kindness_at_work) | `051-84182.en.srt` | 319 | 0:15:36 |
| 052 | [工作不是你的家庭](https://www.ted.com/talks/gloria_chan_packer_work_is_not_your_family_sep_2022) | `052-97793.en.srt` | 307 | 0:15:24 |
| 053 | [总觉得忙碌的真正原因](https://www.ted.com/talks/dorie_clark_the_real_reason_you_feel_so_busy_and_what_to_do_about_it) | `053-90821.en.srt` | 164 | 0:07:42 |
| 054 | [目标感在商业中的力量](https://www.ted.com/talks/ashley_m_grice_the_power_of_purpose_in_business) | `054-89599.en.srt` | 208 | 0:09:36 |
| 055 | [可能改善事业与生活的习惯](https://www.ted.com/talks/paul_catchlove_the_habit_that_could_improve_your_career_and_your_life) | `055-101780.en.srt` | 198 | 0:10:54 |
| 056 | [解决工作问题的五个步骤](https://www.ted.com/talks/anne_morriss_5_steps_to_fix_any_problem_at_work) | `056-111970.en.srt` | 238 | 0:11:48 |
| 057 | [为什么我们都需要情绪急救](https://www.ted.com/talks/guy_winch_why_we_all_need_to_practice_emotional_first_aid) | `057-2193.en.srt` | 327 | 0:17:11 |
| 058 | [情绪勇气的力量](https://www.ted.com/talks/susan_david_the_gift_and_power_of_emotional_courage) | `058-9463.en.srt` | 307 | 0:16:35 |
| 059 | [照顾心理健康并不羞耻](https://www.ted.com/talks/sangu_delle_there_s_no_shame_in_taking_care_of_your_mental_health) | `059-2739.en.srt` | 161 | 0:08:53 |
| 060 | [谈论爱情的一种更好方式](https://www.ted.com/talks/mandy_len_catron_a_better_way_to_talk_about_love) | `060-2661.en.srt` | 293 | 0:15:04 |
| 061 | [不要独自承受抑郁](https://www.ted.com/talks/nikki_webber_allen_don_t_suffer_from_your_depression_in_silence) | `061-2889.en.srt` | 134 | 0:06:19 |
| 062 | [人类情绪的历史](https://www.ted.com/talks/tiffany_watt_smith_the_history_of_human_emotions) | `062-7592.en.srt` | 272 | 0:14:05 |
| 063 | [我们为何愤怒，以及它为何有益](https://www.ted.com/talks/ryan_martin_why_we_get_mad_and_why_it_s_healthy) | `063-41917.en.srt` | 292 | 0:12:53 |
| 064 | [说出自己的真实，也寻找他人的真实](https://www.ted.com/talks/elizabeth_lesser_say_your_truths_and_seek_them_in_others) | `064-2641.en.srt` | 295 | 0:15:31 |
| 065 | [智能设备知道并分享你的哪些信息](https://www.ted.com/talks/kashmir_hill_and_surya_mattu_what_your_smart_devices_know_and_share_about_you) | `065-19927.en.srt` | 207 | 0:08:52 |
| 066 | [小心网络“过滤气泡”](https://www.ted.com/talks/eli_pariser_beware_online_filter_bubbles) | `066-1091.en.srt` | 199 | 0:08:43 |
| 067 | [羞耻的代价](https://www.ted.com/talks/monica_lewinsky_the_price_of_shame) | `067-2217.en.srt` | 347 | 0:21:52 |
| 068 | [怎样在社交媒体上引起关注](https://www.ted.com/talks/alexis_ohanian_how_to_make_a_splash_in_social_media) | `068-714.en.srt` | 95 | 0:04:06 |
| 069 | [是什么让内容广泛传播？](https://www.ted.com/talks/dao_nguyen_what_makes_something_go_viral) | `069-6234.en.srt` | 207 | 0:10:13 |
| 070 | [认知盈余如何改变世界](https://www.ted.com/talks/clay_shirky_how_cognitive_surplus_will_change_the_world) | `070-896.en.srt` | 322 | 0:12:46 |
| 071 | [互联网如何促成亲密关系](https://www.ted.com/talks/stefana_broadbent_how_the_internet_enables_intimacy) | `071-680.en.srt` | 202 | 0:09:30 |
| 072 | [Twitter 用户的声音](https://www.ted.com/talks/evan_williams_the_voices_of_twitter_users) | `072-473.en.srt` | 167 | 0:07:37 |
| 073 | [科技如何应对极端主义与网络骚扰](https://www.ted.com/talks/yasmin_green_how_technology_can_fight_extremism_and_online_harassment) | `073-17237.en.srt` | 264 | 0:13:24 |
| 074 | [社交媒体与性别的终结](https://www.ted.com/talks/johanna_blakley_social_media_and_the_end_of_gender) | `074-1066.en.srt` | 199 | 0:08:06 |
| 075 | [追求无知](https://www.ted.com/talks/stuart_firestein_the_pursuit_of_ignorance) | `075-1827.en.srt` | 417 | 0:18:16 |
| 076 | [我们为什么应该信任科学家](https://www.ted.com/talks/naomi_oreskes_why_we_should_trust_scientists) | `076-2032.en.srt` | 454 | 0:18:57 |
| 077 | [科学为何要求跃入未知](https://www.ted.com/talks/uri_alon_why_science_demands_a_leap_into_the_unknown) | `077-2020.en.srt` | 397 | 0:15:32 |
| 078 | [人体解剖的迷人艺术](https://www.ted.com/talks/vanessa_ruiz_the_spellbinding_art_of_human_anatomy) | `078-2571.en.srt` | 204 | 0:11:07 |
| 079 | [用苹果制造耳朵的科学家](https://www.ted.com/talks/andrew_pelling_this_scientist_makes_ears_out_of_apples) | `079-2502.en.srt` | 147 | 0:06:52 |
| 080 | [哲学早餐俱乐部](https://www.ted.com/talks/laura_snyder_the_philosophical_breakfast_club) | `080-1712.en.srt` | 241 | 0:12:15 |
| 081 | [给年轻科学家的建议](https://www.ted.com/talks/e_o_wilson_advice_to_a_young_scientist) | `081-1485.en.srt` | 253 | 0:14:35 |
| 082 | [玩耍！实验！发现！](https://www.ted.com/talks/kary_mullis_play_experiment_discover) | `082-426.en.srt` | 722 | 0:29:09 |
| 083 | [怎样教计算机理解图像](https://www.ted.com/talks/fei_fei_li_how_we_re_teaching_computers_to_understand_pictures) | `083-2218.en.srt` | 289 | 0:17:45 |
| 084 | [我如何爱上类星体与宇宙（源时长有差异）](https://www.ted.com/talks/jedidah_isler_how_i_fell_in_love_with_quasars_blazars_and_our_incredible_universe) | `084-2237.en.srt` | 74 | 0:04:04 |
| 085 | [爱情的数学](https://www.ted.com/talks/hannah_fry_the_mathematics_of_love) | `085-2153.en.srt` | 336 | 0:16:48 |
| 086 | [黑客：互联网的免疫系统](https://www.ted.com/talks/keren_elazari_hackers_the_internet_s_immune_system) | `086-2019.en.srt` | 372 | 0:16:22 |
| 087 | [童年创伤如何影响一生的健康](https://www.ted.com/talks/nadine_burke_harris_how_childhood_trauma_affects_health_across_a_lifetime) | `087-2194.en.srt` | 245 | 0:15:45 |
| 088 | [细菌怎样“交谈”](https://www.ted.com/talks/bonnie_bassler_how_bacteria_talk) | `088-509.en.srt` | 389 | 0:17:43 |
| 089 | [会闪烁、发声并教学的积木](https://www.ted.com/talks/ayah_bdeir_building_blocks_that_blink_beep_and_teach) | `089-1404.en.srt` | 126 | 0:05:06 |
| 090 | [人类心智的神经画像](https://www.ted.com/talks/nancy_kanwisher_a_neural_portrait_of_the_human_mind) | `090-2077.en.srt` | 434 | 0:17:27 |
| 091 | [数字政变是什么样的](https://www.ted.com/talks/carole_cadwalladr_this_is_what_a_digital_coup_looks_like) | `091-148289.en.srt` | 304 | 0:17:31 |
| 092 | [怎样识别 AI 假照片](https://www.ted.com/talks/hany_farid_how_to_spot_fake_ai_photos) | `092-155789.en.srt` | 235 | 0:12:27 |
| 093 | [读心的艺术](https://www.ted.com/talks/oz_pearlman_the_art_of_reading_minds) | `093-161147.en.srt` | 372 | 0:14:17 |
| 094 | [可能阻止第三次世界大战的 AI 武器](https://www.ted.com/talks/palmer_luckey_the_ai_arsenal_that_could_stop_world_war_iii) | `094-148330.en.srt` | 345 | 0:15:12 |
| 095 | [气候行动为何不可阻挡](https://www.ted.com/talks/al_gore_why_climate_action_is_unstoppable_and_climate_realism_is_a_myth) | `095-155791.en.srt` | 431 | 0:24:01 |
| 096 | [AI 的灾难性风险与更安全的道路](https://www.ted.com/talks/yoshua_bengio_the_catastrophic_risks_of_ai_and_a_safer_path) | `096-148377.en.srt` | 265 | 0:14:48 |
| 097 | [Sam Altman 谈 ChatGPT、AI 智能体与超级智能](https://www.ted.com/talks/sam_altman_openai_s_sam_altman_talks_chatgpt_ai_agents_and_superintelligence_live_at_ted2025) | `097-148296.en.srt` | 1,014 | 0:47:24 |
| 098 | [乌克兰无人机袭击为何改变战争](https://www.ted.com/talks/ian_bremmer_why_ukraine_s_drone_attack_on_russia_changes_war_forever) | `098-148425.en.srt` | 841 | 0:44:56 |
| 099 | [怎样把希望转化为行动？医生与公共卫生专家的对谈](https://www.ted.com/talks/david_fajgenbaum_and_celina_de_sola_how_do_you_turn_hope_into_action_a_doctor_and_a_public_health_expert_answer) | `099-161392.en.srt` | 680 | 0:29:32 |
| 100 | [怎样不再在意他人的看法？电影人与治疗师的对谈](https://www.ted.com/talks/baron_ryan_and_stephanie_r_yates_anyabwile_how_do_you_stop_caring_what_others_think_a_filmmaker_and_a_therapist_answer) | `100-148415.en.srt` | 567 | 0:25:56 |

## 第 084 场：官方源时长差异

官方页面报告 13:32，但官方 transcript、caption JSON 和播放器完整英文 VTT 都只有同样的 74 条字幕，正文到致谢及掌声约 4 分钟。已额外保存 `084-2237.player.en.vtt` 核查；它与 JSON 时间轴相差 3.504 秒的播放器片头。字幕全部保留，不能据此声称覆盖了 13 分钟音视频，也未把目录时长擅自改成 4 分钟。

## 重试与重建

下载脚本会保留已下载的官方原件并继续处理缺失条目：

```bash
python3 references/ted/download_subtitles.py
```

使用边界按 [TED 官方条款](https://www.ted.com/about/our-organization/our-policies-terms/ted-com-terms-of-use) 记录：一般为 CC BY-NC-ND 4.0，具体条目和第三方素材可能另有权利；本批保存在本机供个人学习，原始全文不进 Git。
