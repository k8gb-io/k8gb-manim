from manim import *
import itertools as it
import random
import numpy as np
import os


red = "ffc1b6"

# camera: https://docs.manim.community/en/stable/examples.html#special-camera-settings
# interactions / calls https://docs.manim.community/en/stable/examples.html#pointwithtrace

# todo: add app icon </>
# add k8gb as black box first
# then zoom in into it and show different components: coredns, externaldns

# revealjs plugin https://github.com/RickDW/manim-revealjs

class FailOver(MovingCameraScene):
    config = {
        "font": "Noto Sans",
        "code_font": "Arial Rounded MT Bold",
        "font_color": BLACK,
        "boxes_color": BLACK,
        "color": BLACK,
    }

    def construct(self):
        self.camera.background_color = WHITE
        self.pods()
        # self.display_images()

    def pods(self):
        self.camera.frame.save_state()
        k8s1 = Rectangle(width=8.0, height=5.0, color=FailOver.config["boxes_color"])
        k8s_text1 = Text("Kubernetes", color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        k8s_text1.next_to(k8s1, UP)

        dep1 = RoundedRectangle(width=3.0, height=2.7, stroke_width=1.0, corner_radius=0.5).set_stroke(GRAY, opacity=0.5).shift(UP*0.1+RIGHT*0.1)
        dep_text1 = Text("App Deployment (1 pod)", color=FailOver.config["font_color"], font_size=20, font=FailOver.config["font"])
        dep_text1.next_to(dep1, UP)
        dep_text12 = Text("App Deployment (2 pods)", color=FailOver.config["font_color"], font_size=20, font=FailOver.config["font"])
        dep_text12.next_to(dep1, UP)
        pod11 = Rectangle(width=2.0, height=1.5, color=FailOver.config["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod_text11 = Text("</>", color=BLUE, font_size=35,font=FailOver.config["code_font"], weight=BOLD)
        pod_text11.move_to(pod11)
        pod12 = Rectangle(width=2.0, height=1.5, color=FailOver.config["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod_text12 = Text("</>", color=BLUE, font_size=35, font=FailOver.config["code_font"], weight=BOLD)
        pod_text12.move_to(pod12)
        deployment1 = Group(dep1, pod11, pod_text11)
        pod2group = Group(pod12, pod_text12)
        
        self.play(Create(k8s1))
        self.play(Write(k8s_text1))

        self.play(FadeIn(deployment1), run_time=1.5)
        self.play(FadeIn(dep_text1), run_time=0.5)
        self.play(pod2group.animate.shift(RIGHT*0.2).shift(UP*0.2).set_z(1), TransformMatchingShapes(dep_text1, dep_text12))
        self.wait(1)

        happy_tux = ImageMobject(fr"images/happy_tux.png")
        happy_tux.set_height(1.3)
        happy_tux.to_edge(LEFT)
        self.play(FadeIn(happy_tux))
        dot1 = Dot(color=BLUE)
        dot1.move_to(happy_tux.get_edge_center(RIGHT))
        dot3 = dot1.copy()
        dot2 = dot1.copy().move_to(pod11)
        
        user_interaction = self.say("User sends HTTP requests to app.example.com", False)
        # transformation group
        self.play(Transform(dot1, dot2))
        self.play(Transform(dot1, dot3))
        self.wait(0.7)
        self.play(Transform(dot1, dot2))
        self.play(Transform(dot1, dot3))
        self.play(FadeOut(user_interaction))

        t = self.say("Oh no! Application went down", False)
        self.play(FadeOut(pod_text12))
        self.remove(pod_text11)
        self.play(FadeOut(pod12), run_time=0.5)
        self.play(FadeOut(pod11), run_time=0.5)
        self.play(Transform(dot1, dot2))

        sad_tux = ImageMobject(fr"images/sad_tux.png")
        sad_tux.set_height(1.3)
        sad_tux.to_edge(LEFT)
        self.play(Transform(happy_tux, sad_tux))
        self.play(FadeOut(dot1, sad_tux))
        self.play(FadeOut(t))
        self.say("Let's see how k8gb can help here")
        self.say("First we need to introduce some redundancy, so let's scale up")
        self.play(FadeOut(happy_tux), run_time=0.5)

        # zoom out
        self.play(self.camera.frame.animate.scale(2))
        self.wait(1)

        k8s2 = Rectangle(width=8.0, height=5.0, color=FailOver.config["boxes_color"])
        k8s_text2 = Text("Kubernetes", color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        k8s_text2.next_to(k8s2, UP)

        dep2 = RoundedRectangle(width=3.0, height=2.7, stroke_width=1.0, corner_radius=0.5).set_stroke(GRAY, opacity=0.5).shift(UP*0.1+RIGHT*0.1)
        dep_text2 = Text("App Deployment (2 pods)", color=FailOver.config["font_color"], font_size=20, font=FailOver.config["font"])
        dep_text2.next_to(dep2, UP)

        pod21 = Rectangle(width=2.0, height=1.5, color=FailOver.config["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod22 = Rectangle(width=2.0, height=1.5, color=FailOver.config["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod22.shift(RIGHT*0.2).shift(UP*0.2).set_z(1)
        pod_text22 = Text("</>", color=BLUE, font_size=35, font=FailOver.config["code_font"], weight=BOLD)
        pod_text22.move_to(pod22)

        cl1 = Group(k8s1,k8s_text1,dep1, dep_text12, pod11, pod12, pod_text12)
        cl2 = Group(k8s2,k8s_text2,dep2, dep_text2, pod21, pod22, pod_text22)
        self.add(cl2)
        self.remove(pod_text11)
        self.play(cl2.animate.move_to(RIGHT*4.6 + UP), cl1.animate.move_to(LEFT* 4.6 + UP))
        k8s_text12 = Text("Cluster 1 (eu)", color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        k8s_text22 = Text("Cluster 2 (us)", color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        k8s_text12.next_to(k8s1, UP)
        k8s_text22.next_to(k8s2, UP)
        self.play(TransformMatchingShapes(k8s_text1, k8s_text12), TransformMatchingShapes(k8s_text2, k8s_text22))
        self.wait(1)

        # add k8gb
        self.say_scaled("Add k8gb operator")
        self.play(Group(dep1, dep_text12, pod11, pod12, pod_text12).animate.shift(LEFT*2), Group(dep2, dep_text2, pod21, pod22, pod_text22).animate.shift(LEFT*2))
        k8gb1 = ImageMobject(fr"images/k8gb-logo.png")
        k8gb1.move_to(dep1).shift(RIGHT*4).scale(1.5)
        k8gb2 = ImageMobject(fr"images/k8gb-logo.png")
        k8gb2.move_to(dep2).shift(RIGHT*4).scale(1.5)
        self.play(FadeIn(Group(k8gb1, k8gb2)), run_time=1.5)

        self.say_scaled("Configure k8gb to use edge dns server")
        route = ImageMobject(fr"images/route53.png").scale(0.7)
        route.to_edge(DOWN).shift(DOWN*1.5)
        self.play(FadeIn(route))

        self.say_scaled("Setup load balancing strategy")
        k8s_text13 = Text("Primary Cluster 1 (eu)", color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        k8s_text23 = Text("Secondary Cluster 2 (us)", color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        k8s_text13.next_to(k8s1, UP)
        k8s_text23.next_to(k8s2, UP)
        self.play(TransformMatchingShapes(k8s_text12, k8s_text13), TransformMatchingShapes(k8s_text22, k8s_text23))
        # route_bubble = SpeechBubble()

        self.say_scaled("Let's look how failover strategy works")
        # show tux again
        happy_tux2 = ImageMobject(fr"images/happy_tux.png")
        happy_tux2.scale(0.7)
        happy_tux2.move_to(self.camera.frame.get_left()).shift(RIGHT*1.5+DOWN*3)

        dot_dns = Dot(color=RED, radius=DEFAULT_DOT_RADIUS*2).move_to(self.camera.frame.get_left()).shift(RIGHT*1.5+UP*1)
        dot_http = Dot(color=BLUE, radius=DEFAULT_DOT_RADIUS*2).next_to(dot_dns, direction=DOWN, buff=0.5)
        dot_dns_text = Text("dns resolution", font_size=24, color=RED, font=FailOver.config["font"]).next_to(dot_dns, direction=RIGHT, buff=0.7)
        dot_http_text = Text("HTTP request", font_size=24, color=BLUE, font=FailOver.config["font"]).next_to(dot_http, direction=RIGHT, buff=0.7)
        dot_legend = VGroup(dot_dns, dot_http, dot_dns_text, dot_http_text)
        self.play(FadeIn(happy_tux2, dot_legend), run_time=0.5)

        dot_t = dot1.scale(2).move_to(happy_tux2.get_edge_center(RIGHT)).copy()
        dot_moving = dot_t.copy()
        dot_r = dot_t.copy().move_to(route)
        dot_c1 = dot_t.copy().move_to(pod11)
        dot_c2 = dot_t.copy().move_to(pod21)
        self.play(Transform(dot_moving.set_color(RED), dot_r.set_color(RED)))
        self.play(Transform(dot_moving.set_color(RED), dot_t.set_color(RED)))
        self.wait(0.4)
        self.play(Transform(dot_moving.set_color(BLUE), dot_c1.set_color(BLUE)), run_time=0.5)
        self.play(Transform(dot_moving.set_color(BLUE), dot_t.set_color(BLUE)), run_time=0.5)
        self.play(Transform(dot_moving.set_color(BLUE), dot_c1.set_color(BLUE)), run_time=0.5)
        self.play(Transform(dot_moving.set_color(BLUE), dot_t.set_color(BLUE)), run_time=0.5)
        self.play(Transform(dot_moving.set_color(BLUE), dot_c1.set_color(BLUE)), run_time=0.5)
        self.play(Transform(dot_moving.set_color(BLUE), dot_t.set_color(BLUE)), run_time=0.5)

    def say(self, what, ephemeral=True):
        t = Text(what, color=FailOver.config["font_color"], font_size=23, font=FailOver.config["font"])
        t.to_edge(DR, buff=0.5)
        self.play(Write(t))
        if ephemeral:
            self.wait(1)
            self.play(FadeOut(t))
        else:
            return t

    def say_scaled(self, what, ephemeral=True):
        t = Text(what, color=FailOver.config["font_color"], font_size=46, font=FailOver.config["font"])
        t.move_to(self.camera.frame.get_right() + self.camera.frame.get_bottom()).shift(UP*1.5+LEFT*(t.width*0.6))
        self.play(Write(t))
        if ephemeral:
            self.wait(1)
            self.play(FadeOut(t))
        else:
            return t



