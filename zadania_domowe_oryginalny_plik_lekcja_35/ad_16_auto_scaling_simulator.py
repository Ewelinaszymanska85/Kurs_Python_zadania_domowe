import random
from dataclasses import dataclass, field
from enum import Enum


class ScalingAction(Enum):
    SCALE_UP = "SCALE UP"
    SCALE_DOWN = "SCALE DOWN"
    NO_CHANGE = "NO CHANGE"


@dataclass
class AutoScalingConfig:
    min_instances: int = 1
    max_instances: int = 6
    scale_up_threshold: float = 75.0
    scale_down_threshold: float = 30.0
    required_measurements: int = 3


@dataclass
class ScalingEvent:
    iteration: int
    cpu: float
    instances: int
    action: ScalingAction


def simulate_load() -> float:
    """Zwraca losowe obci─ů┼╝enie CPU w zakresie 20-90%."""
    return round(random.uniform(20, 90), 1)


class AutoScalingSimulator:
    """Symuluje Auto Scaling na podstawie kolejnych pomiar├│w CPU."""

    def __init__(
        self,
        config: AutoScalingConfig,
        instances: int = 2,
    ) -> None:
        self.config = config
        self.instances = instances
        self.high_cpu_count = 0
        self.low_cpu_count = 0
        self.history: list[ScalingEvent] = field(default_factory=list)
        self.history = []

    def evaluate(self, cpu: float) -> ScalingAction:
        if not 0 <= cpu <= 100:
            raise ValueError("CPU musi mie┼Ťci─ç si─Ö w zakresie 0-100%.")

        if cpu >= self.config.scale_up_threshold:
            self.high_cpu_count += 1
            self.low_cpu_count = 0

        elif cpu <= self.config.scale_down_threshold:
            self.low_cpu_count += 1
            self.high_cpu_count = 0

        else:
            self.high_cpu_count = 0
            self.low_cpu_count = 0

        if (
            self.high_cpu_count >= self.config.required_measurements
            and self.instances < self.config.max_instances
        ):
            self.instances += 1
            self.high_cpu_count = 0
            return ScalingAction.SCALE_UP

        if (
            self.low_cpu_count >= self.config.required_measurements
            and self.instances > self.config.min_instances
        ):
            self.instances -= 1
            self.low_cpu_count = 0
            return ScalingAction.SCALE_DOWN

        return ScalingAction.NO_CHANGE

    def run(self, iterations: int = 20) -> None:
        print("=== AUTO SCALING SIMULATOR ===")

        for iteration in range(1, iterations + 1):
            cpu = simulate_load()
            action = self.evaluate(cpu)

            self.history.append(
                ScalingEvent(
                    iteration=iteration,
                    cpu=cpu,
                    instances=self.instances,
                    action=action,
                )
            )

            print(
                f"{iteration:02}. "
                f"CPU: {cpu:5.1f}% | "
                f"Instancje: {self.instances} | "
                f"Akcja: {action.value}"
            )

        print("\n=== PODSUMOWANIE ===")
        print(f"Ko┼äcowa liczba instancji: {self.instances}")

        scaling_events = [e for e in self.history if e.action != ScalingAction.NO_CHANGE]
        print(f"Liczba akcji skalowania: {len(scaling_events)}")

        for event in scaling_events:
            print(
                f"  - Iteracja {event.iteration:02}: {event.action.value} "
                f"(CPU: {event.cpu}%, instancje: {event.instances})"
            )


if __name__ == "__main__":
    configuration = AutoScalingConfig(
        min_instances=1,
        max_instances=6,
        scale_up_threshold=75.0,
        scale_down_threshold=30.0,
        required_measurements=3,
    )

    simulator = AutoScalingSimulator(
        config=configuration,
        instances=2,
    )

    simulator.run(iterations=20)
