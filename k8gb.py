from manim import *

# camera: https://docs.manim.community/en/stable/examples.html#special-camera-settings
# interactions / calls https://docs.manim.community/en/stable/examples.html#pointwithtrace

# add k8gb as black box first
# then zoom in into it and show different components: coredns, externaldns

# revealjs plugin https://github.com/RickDW/manim-revealjs

class FailOver(MovingCameraScene):
    # color scheme: https://www.reddit.com/r/manim/comments/dzxoen/predefined_color_scheme/
    cfg = {
        "font": "Noto Sans",
        "code_font": "Arial Rounded MT Bold",
        "font_color": BLACK,
        "boxes_color": BLACK,
        "dns_color": RED_E,
        "http_color": BLUE,
        "color": BLACK,
    }

    def construct(self):
        self.camera.background_color = WHITE
        self.pods()
        # self.display_images()
        # self.speech_bubble()

    def pods(self):
        self.camera.frame.save_state()
        k8s1 = Rectangle(width=8.0, height=5.0, color=self.cfg["boxes_color"])
        k8s_text1 = Text("Kubernetes", color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        k8s_text1.next_to(k8s1, UP)

        dep1 = RoundedRectangle(width=3.0, height=2.7, stroke_width=1.0, corner_radius=0.5).set_stroke(GRAY, opacity=0.5).shift(UP*0.1+RIGHT*0.1)
        dep_text1 = Text("App Deployment (1 pod)", color=self.cfg["font_color"], font_size=20, font=self.cfg["font"])
        dep_text1.next_to(dep1, UP)
        dep_text12 = Text("App Deployment (2 pods)", color=self.cfg["font_color"], font_size=20, font=self.cfg["font"])
        dep_text12.next_to(dep1, UP)
        pod11 = Rectangle(width=2.0, height=1.5, color=self.cfg["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod_text11 = Text("</>", color=self.cfg["http_color"], font_size=35,font=self.cfg["code_font"], weight=BOLD)
        pod_text11.move_to(pod11)
        pod12 = Rectangle(width=2.0, height=1.5, color=self.cfg["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod_text12 = Text("</>", color=self.cfg["http_color"], font_size=35, font=self.cfg["code_font"], weight=BOLD)
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
        happy_tux.set_height(1.3) # deprecated
        happy_tux.to_edge(LEFT)
        self.play(FadeIn(happy_tux))
        dot1 = Dot(color=self.cfg["http_color"])
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
        self.play(FadeOut(pod_text12), run_time=0.3)
        self.remove(pod_text11)
        self.play(FadeOut(pod12), run_time=0.6)
        self.play(FadeOut(pod11), run_time=0.3)
        dep_text13 = Text("App Deployment (0 pods)", color=self.cfg["font_color"], font_size=20, font=self.cfg["font"]).next_to(dep1, UP)
        self.play(Transform(dep_text12, dep_text13), run_time=0.7)
        self.play(Transform(dot1, dot2))

        sad_tux = ImageMobject(fr"images/sad_tux.png")
        sad_tux.set_height(1.3) # deprecated
        sad_tux.to_edge(LEFT)
        self.play(Transform(happy_tux, sad_tux))
        self.play(FadeOut(t,dot1), run_time=0.5)
        self.say("Let's see how k8gb can help here")
        self.say("First we need to introduce some redundancy, so let's scale up")
        self.play(FadeOut(happy_tux), run_time=0.5)

        # zoom out
        self.play(self.camera.frame.animate.scale(2))
        self.wait(0.2)

        k8s2 = Rectangle(width=8.0, height=5.0, color=self.cfg["boxes_color"])
        k8s_text2 = Text("Kubernetes", color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        k8s_text2.next_to(k8s2, UP)

        dep2 = RoundedRectangle(width=3.0, height=2.7, stroke_width=1.0, corner_radius=0.5).set_stroke(GRAY, opacity=0.5).shift(UP*0.1+RIGHT*0.1)
        dep_text2 = Text("App Deployment (2 pods)", color=self.cfg["font_color"], font_size=20, font=self.cfg["font"])
        dep_text2.next_to(dep2, UP)

        pod21 = Rectangle(width=2.0, height=1.5, color=self.cfg["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod22 = Rectangle(width=2.0, height=1.5, color=self.cfg["boxes_color"], fill_color=WHITE, fill_opacity = 1)
        pod22.shift(RIGHT*0.2).shift(UP*0.2).set_z(1)
        pod_text22 = Text("</>", color=self.cfg["http_color"], font_size=35, font=self.cfg["code_font"], weight=BOLD)
        pod_text22.move_to(pod22)

        dep_text14 = Text("App Deployment (2 pods)", color=self.cfg["font_color"], font_size=20, font=self.cfg["font"]).next_to(dep1, UP)
        cl1 = Group(k8s1,k8s_text1,dep1, dep_text14, pod11, pod12, pod_text12)
        cl2 = Group(k8s2,k8s_text2,dep2, dep_text2, pod21, pod22, pod_text22)
        self.add(cl2)
        self.remove(pod_text11, dep_text12)
        self.play(cl2.animate.move_to(RIGHT*4.6 + UP), cl1.animate.move_to(LEFT* 4.6 + UP))
        k8s_text12 = Text("Cluster 1 (eu)", color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        k8s_text22 = Text("Cluster 2 (us)", color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        k8s_text12.next_to(k8s1, UP)
        k8s_text22.next_to(k8s2, UP)
        self.play(TransformMatchingShapes(k8s_text1, k8s_text12), TransformMatchingShapes(k8s_text2, k8s_text22))
        self.wait(0.5)

        # add k8gb
        self.say_scaled("Add k8gb operator")
        self.play(Group(dep1, dep_text14, pod11, pod12, pod_text12).animate.shift(LEFT*2), Group(dep2, dep_text2, pod21, pod22, pod_text22).animate.shift(LEFT*2))
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
        k8s_text13 = Text("Primary Cluster 1 (eu)", color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        k8s_text23 = Text("Secondary Cluster 2 (us)", color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        k8s_text13.next_to(k8s1, UP)
        k8s_text23.next_to(k8s2, UP)
        self.play(TransformMatchingShapes(k8s_text12, k8s_text13), TransformMatchingShapes(k8s_text22, k8s_text23))

        self.say_scaled("and edge DNS server")
        route_bubble = self.speech_bubble().scale(0.9).next_to(route, direction=RIGHT, buff=0)
        self.play(Create(route_bubble))
        dns_bubble_title = Text("app.example.com", color=self.cfg["dns_color"], font_size=25, font=self.cfg["font"])
        dns_bubble_title.next_to(route_bubble, direction=UP, buff=0.1).shift(RIGHT*0.3)
        self.play(Write(dns_bubble_title))
        dns_bubble_r1 = Text("192.168.0.1 (node @ eu)", color=self.cfg["dns_color"], font_size=17, font=self.cfg["font"])
        # dns_bubble_r2 = Text("192.168.0.2 (node 2 @ eu)", color=self.cfg["dns_color"], font_size=18, font=self.cfg["font"])
        dns_bubble_r1.next_to(dns_bubble_title, direction=DOWN, buff=0.4).shift(RIGHT*0.1)
        # dns_bubble_r2.next_to(dns_bubble_r1, direction=DOWN, buff=0.2)
        ttl_text = Text("(TTL = 30sec)", color=self.cfg["dns_color"], font_size=25, font=self.cfg["font"])
        ttl_text.next_to(route_bubble, direction=RIGHT)
        self.play(Write(dns_bubble_r1), run_time=0.5)
        # self.play(Write(dns_bubble_r2), run_time=0.5)
        self.play(Write(ttl_text), run_time=1)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.35).move_to(route_bubble))
        self.wait(0.2)
        detail_font = 11
        dns_bubble_r1_detailed1 = Text(";; AUTHORITY SECTION:", color=self.cfg["dns_color"], font_size=detail_font, font=self.cfg["font"])
        dns_bubble_r1_detailed2 = Text("example.com. 30 IN NS gslb-ns-us-app.example.com.", color=self.cfg["dns_color"], font_size=detail_font, font=self.cfg["font"])
        dns_bubble_r1_detailed3 = Text("example.com. 30 IN NS gslb-ns-eu-app.example.com.", color=self.cfg["dns_color"], font_size=detail_font, font=self.cfg["font"])
        dns_bubble_r1_detailed4 = Text(";; ADDITIONAL SECTION:", color=self.cfg["dns_color"], font_size=detail_font, font=self.cfg["font"])
        dns_bubble_r1_detailed5 = Text("gslb-ns-us-app.example.com. 30 IN A 10.0.0.1", color=self.cfg["dns_color"], font_size=detail_font, font=self.cfg["font"])
        dns_bubble_r1_detailed6 = Text("gslb-ns-eu-app.example.com. 30 IN A 10.0.1.1", color=self.cfg["dns_color"], font_size=detail_font, font=self.cfg["font"])
        detailed_dns = VGroup(dns_bubble_r1_detailed1,dns_bubble_r1_detailed2,dns_bubble_r1_detailed3,dns_bubble_r1_detailed4,dns_bubble_r1_detailed5,dns_bubble_r1_detailed6)
        detailed_dns.arrange(DOWN, center=False, buff=0.1, aligned_edge=LEFT)
        detailed_dns.next_to(dns_bubble_title, direction=DOWN, buff=0.3).shift(RIGHT*0.2)
        self.play(FadeOut(dns_bubble_r1))
        self.play(FadeIn(detailed_dns))

        self.say_zoomed("In fact it's a glue record that enables the zone delegation")
        self.say_zoomed("Route53 is recursive DNS server delegating the calls for our domain to one of our internal CoreDNS servers", wait=2.7)
        self.say_zoomed("K8gb controller makes sure that CoreDNS contains updated DNS records based on the load balancing strategy", wait=2.7)
        self.say_zoomed("For the sake of simplicity, let's pretend it can directly resolve app.example.com to one of the k8s nodes", wait=2.7)
        self.play(FadeOut(detailed_dns))
        self.play(FadeIn(dns_bubble_r1))
        self.play(Restore(self.camera.frame))

        self.say_scaled("Let's look how failover strategy works")
        # show tux again
        happy_tux2 = ImageMobject(fr"images/happy_tux.png")
        happy_tux2.scale(0.7)
        happy_tux2.move_to(self.camera.frame.get_left()).shift(RIGHT*1.5+DOWN*3)
        happy_tux2_orig = happy_tux2.copy()

        dot_dns = Dot(color=self.cfg["dns_color"], radius=DEFAULT_DOT_RADIUS*2).move_to(self.camera.frame.get_left()).shift(RIGHT*1.5+UP*1)
        dot_http = Dot(color=self.cfg["http_color"], radius=DEFAULT_DOT_RADIUS*2).next_to(dot_dns, direction=DOWN, buff=0.5)
        dot_dns_text = Text("dns resolution", font_size=24, color=self.cfg["dns_color"], font=self.cfg["font"]).next_to(dot_dns, direction=RIGHT, buff=0.7)
        dot_http_text = Text("HTTP request", font_size=24, color=self.cfg["http_color"], font=self.cfg["font"]).next_to(dot_http, direction=RIGHT, buff=0.7)
        dot_legend = VGroup(dot_dns, dot_http, dot_dns_text, dot_http_text)
        self.play(FadeIn(happy_tux2, dot_legend), run_time=0.5)

        dot_t = dot1.scale(2).move_to(happy_tux2.get_edge_center(RIGHT)).copy()
        dot_moving = dot_t.copy()
        dot_r = dot_t.copy().move_to(route)
        dot_c1 = dot_t.copy().move_to(pod11)
        dot_c2 = dot_t.copy().move_to(pod21)
        self.say_scaled("Tux wants to send http request to app.example.com")
        self.say_scaled("He asks the Route53 to resolve 'app.example.com'")
        self.play(Transform(dot_moving.set_color(self.cfg["dns_color"]), dot_r.set_color(self.cfg["dns_color"])))
        self.play(Transform(dot_moving.set_color(self.cfg["dns_color"]), dot_t.set_color(self.cfg["dns_color"])))
        self.wait(0.4)
        self.say_scaled("For the next 30 seconds it's 192.168.0.1")
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_c1.set_color(self.cfg["http_color"])), run_time=0.5)
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_t.set_color(self.cfg["http_color"])), run_time=0.5)
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_c1.set_color(self.cfg["http_color"])), run_time=0.5)
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_t.set_color(self.cfg["http_color"])), run_time=0.5)
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_c1.set_color(self.cfg["http_color"])), run_time=0.5)
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_t.set_color(self.cfg["http_color"])), run_time=0.5)
        self.say_scaled("Oh no! The pods on cluster in eu went down.")

        # scale pods on cl1 to 0
        self.play(FadeOut(VGroup(pod_text12, pod12, pod11)))
        dep_text13.next_to(dep1, UP)
        self.play(Transform(dep_text14, dep_text13))

        # make tux sad
        sad_tux2 = ImageMobject(fr"images/sad_tux.png")
        sad_tux2.scale(0.7)
        sad_tux2.move_to(self.camera.frame.get_left()).shift(RIGHT*1.5+DOWN*3)
        self.play(Transform(happy_tux2, sad_tux2), run_time=1.5)

        self.say_scaled("Luckily, k8gb controller on cluster 1 kicks in")
        self.play(Wiggle(k8gb1))

        self.say_scaled("and updates the DNS records to point to cluster 2")
        # change the records in the bubble
        dns_bubble_r3 = Text("192.168.1.1 (node @ us)", color=self.cfg["dns_color"], font_size=17, font=self.cfg["font"])
        # dns_bubble_r4 = Text("192.168.1.2 (node 2 @ us)", color=self.cfg["dns_color"], font_size=18, font=self.cfg["font"])
        dns_bubble_r3.next_to(dns_bubble_title, direction=DOWN, buff=0.4).shift(RIGHT*0.1)
        # dns_bubble_r4.next_to(dns_bubble_r1, direction=DOWN, buff=0.2)
        self.play(Unwrite(dns_bubble_r1), run_time=0.5)
        # self.play(Unwrite(dns_bubble_r2), run_time=0.5)
        self.play(Write(dns_bubble_r3), run_time=0.5)
        # self.play(Write(dns_bubble_r4), run_time=0.5)

        self.say_scaled("When TTL expires, Tux creates another DNS request")

        self.play(Transform(dot_moving.set_color(self.cfg["dns_color"]), dot_r.set_color(self.cfg["dns_color"])))
        self.play(Transform(dot_moving.set_color(self.cfg["dns_color"]), dot_t.set_color(self.cfg["dns_color"])))
        self.say_scaled("and starts communicating with the correct cluster")
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_c2.set_color(self.cfg["http_color"])))
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_t.set_color(self.cfg["http_color"])))
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_c2.set_color(self.cfg["http_color"])))
        self.play(Transform(dot_moving.set_color(self.cfg["http_color"]), dot_t.set_color(self.cfg["http_color"])))
        
        # make tux happy
        self.play(Transform(happy_tux2, happy_tux2_orig), run_time=1.5)
        self.say_scaled("Cluster in 'us' took over all the communication and Tux is happy again")
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
        self.play(FadeIn(ImageMobject(fr"images/k8gb-logo.png").scale(2.5)))
        self.play(Write(Text("k8gb.io", color=self.cfg["font_color"], font_size=55, font=self.cfg["font"]).shift(DOWN*2)), run_time=1.5)
        self.wait()


    def say_zoomed(self, what, ephemeral=True, wait=1.5):
        t = Text(what, color=self.cfg["font_color"], font_size=14, font=self.cfg["font"])
        t.move_to(self.camera.frame.get_right() + self.camera.frame.get_bottom()).shift(UP*4.5+LEFT*(4.8+t.width*0.48))
        self.play(Write(t))
        if ephemeral:
            self.wait(wait)
            self.play(FadeOut(t))
        else:
            return t

    def say(self, what, ephemeral=True):
        t = Text(what, color=self.cfg["font_color"], font_size=23, font=self.cfg["font"])
        t.to_edge(DR, buff=0.5)
        self.play(Write(t))
        if ephemeral:
            self.wait(1)
            self.play(FadeOut(t))
        else:
            return t

    def say_scaled(self, what, ephemeral=True):
        t = Text(what, color=self.cfg["font_color"], font_size=46, font=self.cfg["font"])
        t.move_to(self.camera.frame.get_right() + self.camera.frame.get_bottom()).shift(UP*1.5+LEFT*(t.width*0.6))
        self.play(Write(t))
        if ephemeral:
            self.wait(1)
            self.play(FadeOut(t))
        else:
            return t

    def speech_bubble(self):
        Hexagon = [(0,0,0),
            (1.0,-0.1, 0),
            (1.0, 0.7, 0),
            (5.9, 0.7, 0),
            (5.9,-1.7, 0),
            (1.0,-1.7, 0),
            (1.0,-0.55,0),
        ]
        return Polygon(*Hexagon, color=self.cfg["dns_color"])
