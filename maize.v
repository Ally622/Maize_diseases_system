(*
  Maize Diseases Knowledge Base in Coq
  ------------------------------------
  This code models diseases, symptoms, conditions, rules, and inference patterns.
*)

(* ----------------------------- *)
(* 1. Ontology                   *)
(* ----------------------------- *)

Inductive Disease :=
  | MLND
  | Rust
  | Blight
  | Smut
  | DownyMildew
  | GrayLeafSpot
  | Anthracnose
  | RootRot
  | EarRot
  | CommonBunt
  | StalkRot
  | ViralStreak
  | LeafCurl
  | Wilt
  | StripeDisease
  | ChlorosisComplex
  | MosaicVirus
  | FusariumWilt
  | AspergillusRot
  | DiplodiaEarRot.

Inductive Symptom :=
  | Yellowing
  | Necrosis
  | LeafSpots
  | StemBreakage
  | EarDiscoloration
  | WhiteFungalGrowth
  | RustPustules
  | MoldyKernels
  | Wilting
  | Curling
  | Streaks
  | SoftRot
  | Blisters
  | PowderyGrowth
  | WaterSoaking
  | DampingOff
  | GrayLesions
  | DeadTissue
  | StuntedGrowth
  | Browning.

Inductive Condition :=
  | HighHumidity
  | LowHumidity
  | ModerateHumidity
  | HighTemp
  | LowTemp
  | WetSoils
  | PoorDrainage
  | Drought
  | InsectVector
  | DensePlanting
  | PoorFertility
  | LatePlanting
  | EarlyPlanting
  | ContaminatedSeed
  | MechanicalInjury.


(* ----------------------------- *)
(* 2. Predicates                 *)
(* ----------------------------- *)

Inductive has_symptom : Disease -> Symptom -> Prop := .
Inductive indicates : Symptom -> Disease -> Prop := .
Inductive triggered_by : Disease -> Condition -> Prop := .
Inductive risk_factor : Disease -> Condition -> Prop := .
Inductive co_occurs : Disease -> Disease -> Prop := .
Inductive severe_under : Disease -> Condition -> Prop := .
Inductive mild_under : Disease -> Condition -> Prop := .

(* Logical implication wrapper *)
Inductive implies_rule : Prop -> Prop -> Prop :=
  mk_implication : forall A B, (A -> B) -> implies_rule A B.


(* ----------------------------- *)
(* 3. Facts —  Rules         *)
(* ----------------------------- *)

(* 3A — Disease → Symptom Facts (30) *)

Constructor hs1  : has_symptom MLND Yellowing.
Constructor hs2  : has_symptom MLND Necrosis.
Constructor hs3  : has_symptom MLND StuntedGrowth.
Constructor hs4  : has_symptom Rust RustPustules.
Constructor hs5  : has_symptom Rust LeafSpots.
Constructor hs6  : has_symptom Blight LeafSpots.
Constructor hs7  : has_symptom Blight DeadTissue.
Constructor hs8  : has_symptom Smut Blisters.
Constructor hs9  : has_symptom Smut MoldyKernels.
Constructor hs10 : has_symptom DownyMildew WhiteFungalGrowth.
Constructor hs11 : has_symptom DownyMildew WaterSoaking.
Constructor hs12 : has_symptom GrayLeafSpot GrayLesions.
Constructor hs13 : has_symptom GrayLeafSpot DeadTissue.
Constructor hs14 : has_symptom Anthracnose DeadTissue.
Constructor hs15 : has_symptom RootRot SoftRot.
Constructor hs16 : has_symptom RootRot Browning.
Constructor hs17 : has_symptom EarRot MoldyKernels.
Constructor hs18 : has_symptom EarRot EarDiscoloration.
Constructor hs19 : has_symptom StalkRot StemBreakage.
Constructor hs20 : has_symptom ViralStreak Streaks.
Constructor hs21 : has_symptom LeafCurl Curling.
Constructor hs22 : has_symptom Wilt Wilting.
Constructor hs23 : has_symptom StripeDisease Streaks.
Constructor hs24 : has_symptom ChlorosisComplex Yellowing.
Constructor hs25 : has_symptom MosaicVirus Yellowing.
Constructor hs26 : has_symptom FusariumWilt Wilting.
Constructor hs27 : has_symptom AspergillusRot MoldyKernels.
Constructor hs28 : has_symptom DiplodiaEarRot MoldyKernels.
Constructor hs29 : has_symptom DiplodiaEarRot EarDiscoloration.
Constructor hs30 : has_symptom Anthracnose Browning.


(* 3B — Symptom → Disease (Indication Rules) (20) *)

Constructor ind1  : indicates Yellowing ChlorosisComplex.
Constructor ind2  : indicates Yellowing MLND.
Constructor ind3  : indicates Necrosis MLND.
Constructor ind4  : indicates RustPustules Rust.
Constructor ind5  : indicates LeafSpots Blight.
Constructor ind6  : indicates LeafSpots Rust.
Constructor ind7  : indicates MoldyKernels EarRot.
Constructor ind8  : indicates MoldyKernels AspergillusRot.
Constructor ind9  : indicates WaterSoaking DownyMildew.
Constructor ind10 : indicates GrayLesions GrayLeafSpot.
Constructor ind11 : indicates Blisters Smut.
Constructor ind12 : indicates SoftRot RootRot.
Constructor ind13 : indicates Streaks ViralStreak.
Constructor ind14 : indicates Streaks StripeDisease.
Constructor ind15 : indicates Curling LeafCurl.
Constructor ind16 : indicates Wilting Wilt.
Constructor ind17 : indicates Wilting FusariumWilt.
Constructor ind18 : indicates Browning RootRot.
Constructor ind19 : indicates DeadTissue Anthracnose.
Constructor ind20 : indicates GrayLesions GrayLeafSpot.


(* 3C — Conditions Trigger Diseases (20) *)

Constructor tr1  : triggered_by MLND InsectVector.
Constructor tr2  : triggered_by Rust HighHumidity.
Constructor tr3  : triggered_by Rust ModerateHumidity.
Constructor tr4  : triggered_by Blight HighHumidity.
Constructor tr5  : triggered_by DownyMildew HighHumidity.
Constructor tr6  : triggered_by DownyMildew WetSoils.
Constructor tr7  : triggered_by GrayLeafSpot HighTemp.
Constructor tr8  : triggered_by Smut ContaminatedSeed.
Constructor tr9  : triggered_by RootRot PoorDrainage.
Constructor tr10 : triggered_by RootRot WetSoils.
Constructor tr11 : triggered_by EarRot HighHumidity.
Constructor tr12 : triggered_by EarRot MechanicalInjury.
Constructor tr13 : triggered_by Wilt Drought.
Constructor tr14 : triggered_by LeafCurl InsectVector.
Constructor tr15 : triggered_by MosaicVirus InsectVector.
Constructor tr16 : triggered_by FusariumWilt WetSoils.
Constructor tr17 : triggered_by StalkRot HighTemp.
Constructor tr18 : triggered_by Anthracnose HighHumidity.
Constructor tr19 : triggered_by AspergillusRot HighTemp.
Constructor tr20 : triggered_by DiplodiaEarRot HighHumidity.


(* 3D — Risk Factors (15) *)

Constructor rf1  : risk_factor MLND LatePlanting.
Constructor rf2  : risk_factor MLND DensePlanting.
Constructor rf3  : risk_factor Rust HighHumidity.
Constructor rf4  : risk_factor Blight HighHumidity.
Constructor rf5  : risk_factor DownyMildew WetSoils.
Constructor rf6  : risk_factor GrayLeafSpot HighTemp.
Constructor rf7  : risk_factor Smut ContaminatedSeed.
Constructor rf8  : risk_factor RootRot PoorDrainage.
Constructor rf9  : risk_factor EarRot HighHumidity.
Constructor rf10 : risk_factor Wilt Drought.
Constructor rf11 : risk_factor MosaicVirus InsectVector.
Constructor rf12 : risk_factor FusariumWilt PoorDrainage.
Constructor rf13 : risk_factor StalkRot HighTemp.
Constructor rf14 : risk_factor DiplodiaEarRot MechanicalInjury.
Constructor rf15 : risk_factor AspergillusRot HighTemp.


(* 3E — Co-occurrence Rules (10) *)

Constructor co1 : co_occurs Rust GrayLeafSpot.
Constructor co2 : co_occurs EarRot AspergillusRot.
Constructor co3 : co_occurs Smut EarRot.
Constructor co4 : co_occurs DownyMildew Blight.
Constructor co5 : co_occurs RootRot FusariumWilt.
Constructor co6 : co_occurs MLND MosaicVirus.
Constructor co7 : co_occurs Anthracnose GrayLeafSpot.
Constructor co8 : co_occurs StalkRot RootRot.
Constructor co9 : co_occurs DiplodiaEarRot AspergillusRot.
Constructor co10: co_occurs Blight Rust.


(* 3F — Severity Rules (10) *)

Constructor sev1  : severe_under MLND HighHumidity.
Constructor sev2  : severe_under Rust HighHumidity.
Constructor sev3  : severe_under DownyMildew WetSoils.
Constructor sev4  : severe_under GrayLeafSpot HighTemp.
Constructor sev5  : severe_under StalkRot HighTemp.
Constructor sev6  : severe_under EarRot HighHumidity.
Constructor sev7  : severe_under FusariumWilt WetSoils.
Constructor sev8  : severe_under Anthracnose HighHumidity.
Constructor sev9  : severe_under DiplodiaEarRot HighHumidity.
Constructor sev10 : severe_under AspergillusRot HighTemp.


(* ----------------------------- *)
(* 4. Inference Rules (15)       *)
(* ----------------------------- *)

Theorem rule1 :
  forall D S, has_symptom D S -> indicates S D.
Proof. (* not guaranteed true; placeholder *) Admitted.

Theorem rule2 :
  forall D C, triggered_by D C -> risk_factor D C.
Proof. Admitted.

Theorem rule3 :
  forall D1 D2 C, triggered_by D1 C -> co_occurs D1 D2 -> triggered_by D2 C.
Proof. Admitted.

Theorem rule4 :
  forall D S C, has_symptom D S -> triggered_by D C -> severe_under D C.
Proof. Admitted.

Theorem rule5 :
  forall D C, risk_factor D C -> severe_under D C.
Proof. Admitted.

Theorem rule6 :
  forall S1 S2 D, indicates S1 D -> indicates S2 D -> has_symptom D S1.
Proof. Admitted.

Theorem rule6 :
  forall S1 S2 D, indicates S1 D -> indicates S2 D -> has_symptom D S1.
Proof. Admitted.

Theorem rule8 :
  forall D S C, has_symptom D S -> severe_under D C -> indicates S D.
Proof. Admitted.

Theorem rule9 :
  forall D C1 C2, triggered_by D C1 -> risk_factor D C2 -> severe_under D C1.
Proof. Admitted.

Theorem rule10 :
  forall D S, has_symptom D S -> indicates S D.
Proof. Admitted.

Theorem rule11 :
  forall D C, severe_under D C -> triggered_by D C.
Proof. Admitted.

Theorem rule12 :
  forall D1 D2 S, has_symptom D1 S -> co_occurs D1 D2 -> has_symptom D2 S.
Proof. Admitted.

Theorem rule13 :
  forall D S C, indicates S D -> risk_factor D C -> severe_under D C.
Proof. Admitted.

Theorem rule14 :
  forall D C, triggered_by D C -> severe_under D C.
Proof. Admitted.

Theorem rule15 :
  forall S D1 D2, indicates S D1 -> co_occurs D1 D2 -> indicates S D2.
Proof. Admitted.


(* ----------------------------- *)
(* 5. Example Queries             *)
(* ----------------------------- *)

Theorem query1 :
  has_symptom Rust LeafSpots.
Proof. apply hs5. Qed.

Theorem query2 :
  indicates Streaks ViralStreak.
Proof. apply ind13. Qed.

Theorem query3 :
  triggered_by DownyMildew WetSoils.
Proof. apply tr6. Qed.

Theorem query4 :
  severe_under FusariumWilt WetSoils.
Proof. apply sev7. Qed.

Theorem query5 :
  co_occurs Rust GrayLeafSpot.
Proof. apply co1. Qed.

