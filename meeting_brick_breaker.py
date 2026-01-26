"""Meeting Brick Breaker Game.

Este script implementa un juego tipo brick breaker inspirado en la agenda de reuniones
que aparece en la captura proporcionada. Cada ladrillo representa uno de los bloques
(calendario) que hay que "liberar" golpeándolo con la pelota.

Requisitos:
    pip install pygame

Ejecución:
    python meeting_brick_breaker.py
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pygame


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
FPS = 60

BACKGROUND_COLOR = (12, 21, 45)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (236, 196, 83)
TEXT_COLOR = (230, 230, 230)
COLUMN_GAP = 6
ROW_GAP = 6

DAYS = [
    "Lunes 29",
    "Martes 30",
    "Miércoles 31",
    "Jueves 01",
    "Viernes 02",
    "Sábado 03",
]


@dataclass
class MeetingBlock:
    """Representa un bloque de reunión de la agenda."""

    day: str
    title: str
    start: str
    duration_minutes: int
    location: str
    color: Tuple[int, int, int]


MEETINGS: List[MeetingBlock] = [
    MeetingBlock(
        day="Lunes 29",
        title="Daily comité inversiones (Cancelada)",
        start="09:30",
        duration_minutes=60,
        location="Microsoft Teams",
        color=(143, 150, 201),
    ),
    MeetingBlock(
        day="Lunes 29",
        title="Revisión bloques archivo normativo",
        start="11:30",
        duration_minutes=90,
        location="Sala híbrida",
        color=(174, 112, 158),
    ),
    MeetingBlock(
        day="Lunes 29",
        title="Espacio para foco (sin reuniones)",
        start="14:00",
        duration_minutes=180,
        location="Sin sala",
        color=(98, 123, 172),
    ),
    MeetingBlock(
        day="Martes 30",
        title="Daily comité inversiones",
        start="09:30",
        duration_minutes=60,
        location="Microsoft Teams",
        color=(143, 150, 201),
    ),
    MeetingBlock(
        day="Martes 30",
        title="Extensión modelos de riesgo",
        start="11:00",
        duration_minutes=90,
        location="Teams",
        color=(219, 128, 108),
    ),
    MeetingBlock(
        day="Martes 30",
        title="Reunión OC",
        start="15:00",
        duration_minutes=60,
        location="Sala 3C",
        color=(174, 112, 158),
    ),
    MeetingBlock(
        day="Martes 30",
        title="Espacio documentación",
        start="16:30",
        duration_minutes=90,
        location="Escritorio",
        color=(98, 123, 172),
    ),
    MeetingBlock(
        day="Miércoles 31",
        title="Daily comité inversiones",
        start="09:30",
        duration_minutes=60,
        location="Microsoft Teams",
        color=(143, 150, 201),
    ),
    MeetingBlock(
        day="Miércoles 31",
        title="Reunión SAC con stakeholders",
        start="11:00",
        duration_minutes=120,
        location="Teams",
        color=(219, 128, 108),
    ),
    MeetingBlock(
        day="Miércoles 31",
        title="One on one",
        start="15:00",
        duration_minutes=60,
        location="Teams",
        color=(174, 112, 158),
    ),
    MeetingBlock(
        day="Jueves 01",
        title="Daily comité inversiones",
        start="09:30",
        duration_minutes=60,
        location="Microsoft Teams",
        color=(143, 150, 201),
    ),
    MeetingBlock(
        day="Jueves 01",
        title="Reunión Microsoft Teams",  # Cancelada según la captura
        start="12:00",
        duration_minutes=60,
        location="Microsoft Teams",
        color=(120, 120, 120),
    ),
    MeetingBlock(
        day="Jueves 01",
        title="Comité Arquitectura",
        start="15:00",
        duration_minutes=90,
        location="Sala híbrida",
        color=(98, 123, 172),
    ),
    MeetingBlock(
        day="Viernes 02",
        title="Daily comité inversiones",
        start="09:30",
        duration_minutes=60,
        location="Microsoft Teams",
        color=(143, 150, 201),
    ),
    MeetingBlock(
        day="Viernes 02",
        title="Revisión propuesta bases de datos",
        start="12:00",
        duration_minutes=60,
        location="Teams",
        color=(219, 128, 108),
    ),
    MeetingBlock(
        day="Viernes 02",
        title="Espacio libre",
        start="15:00",
        duration_minutes=180,
        location="--",
        color=(98, 123, 172),
    ),
    MeetingBlock(
        day="Sábado 03",
        title="Sin reuniones",
        start="00:00",
        duration_minutes=720,
        location="Descanso",
        color=(55, 80, 120),
    ),
]


class Paddle:
    def __init__(self, width: int = 120, height: int = 16) -> None:
        self.rect = pygame.Rect(
            WINDOW_WIDTH // 2 - width // 2, WINDOW_HEIGHT - 60, width, height
        )
        self.speed = 420

    def update(self, delta: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= int(self.speed * delta)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += int(self.speed * delta)
        self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.rect.width))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, PADDLE_COLOR, self.rect, border_radius=6)


class Ball:
    def __init__(self) -> None:
        self.radius = 10
        self.reset()

    def reset(self) -> None:
        self.pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        angle = random.uniform(math.pi / 4, 3 * math.pi / 4)
        self.velocity = pygame.Vector2(math.cos(angle), -abs(math.sin(angle))) * 360

    def update(self, delta: float) -> None:
        self.pos += self.velocity * delta

        if self.pos.x - self.radius <= 0 and self.velocity.x < 0:
            self.velocity.x *= -1
        if self.pos.x + self.radius >= WINDOW_WIDTH and self.velocity.x > 0:
            self.velocity.x *= -1
        if self.pos.y - self.radius <= 0 and self.velocity.y < 0:
            self.velocity.y *= -1

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, BALL_COLOR, self.pos, self.radius)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.pos.x - self.radius),
            int(self.pos.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )


class Brick:
    def __init__(self, rect: pygame.Rect, meeting: MeetingBlock) -> None:
        self.rect = rect
        self.meeting = meeting
        self.active = True

    def draw(
        self,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        header_font: pygame.font.Font,
    ) -> None:
        if not self.active and self.meeting.title not in DAYS:
            return

        base_color = self.meeting.color
        if not self.active:
            base_color = tuple(max(channel - 90, 20) for channel in base_color)

        pygame.draw.rect(surface, base_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (15, 15, 25), self.rect, 2, border_radius=8)

        if self.meeting.title in DAYS:
            title_surface = header_font.render(self.meeting.title, True, TEXT_COLOR)
            surface.blit(
                title_surface,
                title_surface.get_rect(center=(self.rect.centerx, self.rect.centery)),
            )
            return

        title_surface = body_font.render(self.meeting.title, True, (15, 15, 25))
        surface.blit(
            title_surface,
            title_surface.get_rect(
                midtop=(self.rect.centerx, self.rect.y + 12),
            ),
        )

        info = f"{self.meeting.start} · {self.meeting.location}".strip()
        info_surface = body_font.render(info, True, (20, 20, 40))
        surface.blit(
            info_surface,
            info_surface.get_rect(midbottom=(self.rect.centerx, self.rect.bottom - 12)),
        )


class MeetingBrickBreaker:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Meeting Brick Breaker")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Roboto", 16)
        self.small_font = pygame.font.SysFont("Roboto", 14)
        self.header_font = pygame.font.SysFont("Roboto", 18, bold=True)
        self.big_font = pygame.font.SysFont("Roboto", 32, bold=True)

        self.paddle = Paddle()
        self.ball = Ball()

        self.lives = 3
        self.score = 0
        self.streak = 0

        self.bricks = self._create_bricks()
        self.meeting_bricks = [
            brick for brick in self.bricks if brick.meeting.title not in DAYS
        ]
        self.cleared_meetings = 0
        self.last_meeting: MeetingBlock | None = None

    def _create_bricks(self) -> List[Brick]:
        bricks: List[Brick] = []
        day_to_meetings: Dict[str, List[MeetingBlock]] = {day: [] for day in DAYS}
        for meeting in MEETINGS:
            day_to_meetings.setdefault(meeting.day, []).append(meeting)

        column_width = (WINDOW_WIDTH - (len(DAYS) + 1) * COLUMN_GAP) / len(DAYS)
        top_offset = 80
        minutes_per_pixel = 1.3

        for index, day in enumerate(DAYS):
            meetings = sorted(
                day_to_meetings.get(day, []), key=lambda m: m.start
            )
            column_x = int(COLUMN_GAP + index * (column_width + COLUMN_GAP))
            day_label_rect = pygame.Rect(column_x, 20, int(column_width), 40)
            bricks.append(
                Brick(
                    rect=day_label_rect,
                    meeting=MeetingBlock(
                        day=day,
                        title=day,
                        start="",
                        duration_minutes=0,
                        location="",
                        color=(40, 60, 100),
                    ),
                )
            )

            y_offset = top_offset
            for meeting in meetings:
                height = max(
                    36, min(int(meeting.duration_minutes * minutes_per_pixel), 280)
                )
                rect = pygame.Rect(
                    column_x,
                    int(y_offset),
                    int(column_width),
                    height,
                )
                bricks.append(Brick(rect, meeting))
                y_offset += height + ROW_GAP
        # Remove inactive day labels from scoring (always active, but not scorable)
        return bricks

    def run(self) -> None:
        running = True
        while running:
            delta = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.lives <= 0 or self._all_meetings_cleared():
                self._render_end_screen()
                pygame.display.flip()
                continue

            self.paddle.update(delta)
            self.ball.update(delta)

            if self.ball.rect.colliderect(self.paddle.rect) and self.ball.velocity.y > 0:
                overlap = self.ball.rect.centerx - self.paddle.rect.centerx
                normalized = overlap / (self.paddle.rect.width / 2)
                bounce_angle = normalized * math.radians(70)
                speed = self.ball.velocity.length()
                self.ball.velocity.x = math.sin(bounce_angle) * speed
                self.ball.velocity.y = -abs(math.cos(bounce_angle) * speed)

            if self.ball.pos.y - self.ball.radius > WINDOW_HEIGHT:
                self.lives -= 1
                self.streak = 0
                self.ball.reset()

            for brick in self.bricks:
                if not brick.active:
                    continue
                if brick.meeting.title in DAYS:
                    # Las etiquetas de los días son decorativas, no cuentan como ladrillos
                    continue
                if brick.rect.colliderect(self.ball.rect):
                    self._handle_ball_brick_collision(brick)
                    break

            self._render()
            pygame.display.flip()

        pygame.quit()

    def _all_meetings_cleared(self) -> bool:
        return all(
            not brick.active or brick.meeting.title in DAYS for brick in self.bricks
        )

    def _handle_ball_brick_collision(self, brick: Brick) -> None:
        brick.active = False
        self.score += 100
        self.streak += 1
        self.cleared_meetings += 1
        self.last_meeting = brick.meeting
        ball_rect = self.ball.rect
        overlap_left = ball_rect.right - brick.rect.left
        overlap_right = brick.rect.right - ball_rect.left
        overlap_top = ball_rect.bottom - brick.rect.top
        overlap_bottom = brick.rect.bottom - ball_rect.top
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left:
            self.ball.pos.x = brick.rect.left - self.ball.radius
            self.ball.velocity.x = -abs(self.ball.velocity.x)
        elif min_overlap == overlap_right:
            self.ball.pos.x = brick.rect.right + self.ball.radius
            self.ball.velocity.x = abs(self.ball.velocity.x)
        elif min_overlap == overlap_top:
            self.ball.pos.y = brick.rect.top - self.ball.radius
            self.ball.velocity.y = -abs(self.ball.velocity.y)
        else:
            self.ball.pos.y = brick.rect.bottom + self.ball.radius
            self.ball.velocity.y = abs(self.ball.velocity.y)

    def _render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        for brick in self.bricks:
            brick.draw(self.screen, self.small_font, self.header_font)

        hud_rect = pygame.Rect(0, WINDOW_HEIGHT - 120, WINDOW_WIDTH, 120)
        pygame.draw.rect(self.screen, (18, 28, 55), hud_rect)
        pygame.draw.line(
            self.screen,
            (35, 50, 90),
            (0, WINDOW_HEIGHT - 120),
            (WINDOW_WIDTH, WINDOW_HEIGHT - 120),
            2,
        )

        if self.last_meeting:
            last_text = self.font.render(
                f"Última reunión liberada: {self.last_meeting.title}",
                True,
                TEXT_COLOR,
            )
            self.screen.blit(last_text, (20, WINDOW_HEIGHT - 105))

        progress = f"{self.cleared_meetings}/{len(self.meeting_bricks)}"
        score_text = self.font.render(
            f"Reuniones liberadas: {progress}", True, TEXT_COLOR
        )
        lives_text = self.font.render(f"Intentos restantes: {self.lives}", True, TEXT_COLOR)
        streak_text = self.font.render(f"Racha: {self.streak}", True, TEXT_COLOR)
        instruction_text = self.font.render(
            "← → / A D para mover | Rompe todos los bloques de reuniones", True, TEXT_COLOR
        )

        self.screen.blit(score_text, (20, WINDOW_HEIGHT - 40))
        self.screen.blit(lives_text, (320, WINDOW_HEIGHT - 40))
        self.screen.blit(streak_text, (620, WINDOW_HEIGHT - 40))
        self.screen.blit(instruction_text, (20, WINDOW_HEIGHT - 70))

    def _render_end_screen(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        if self.lives <= 0:
            title = "La agenda te ganó 😵"
            subtitle = "Repite el intento para liberar todas las reuniones"
        else:
            title = "¡Agenda despejada!"
            subtitle = "Todas las reuniones fueron eliminadas"

        title_surface = self.big_font.render(title, True, TEXT_COLOR)
        subtitle_surface = self.font.render(subtitle, True, TEXT_COLOR)
        restart_surface = self.font.render(
            "Pulsa ESPACIO para reiniciar o ESC para salir", True, TEXT_COLOR
        )

        self.screen.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40)))
        self.screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)))
        self.screen.blit(restart_surface, restart_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self._reset_game()
        elif keys[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _reset_game(self) -> None:
        self.ball.reset()
        self.lives = 3
        self.score = 0
        self.streak = 0
        self.cleared_meetings = 0
        self.last_meeting = None
        for brick in self.bricks:
            brick.active = True


if __name__ == "__main__":
    game = MeetingBrickBreaker()
    game.run()
