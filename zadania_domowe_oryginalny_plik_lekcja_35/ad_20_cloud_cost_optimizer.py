from dataclasses import dataclass
from pathlib import Path


@dataclass
class EC2Instance:
    instance_id: str
    instance_type: str
    state: str
    running_hours_monthly: int
    cpu_usage: float
    monthly_cost: float
    attached_volume_gb: int = 0


class CloudCostOptimizer:
    """Analizuje zasoby EC2 i generuje rekomendacje oszczędności."""

    def __init__(
        self,
        low_usage_threshold: float = 20.0,
        report_file: str = "cloud_cost_report.md",
    ) -> None:
        self.low_usage_threshold = low_usage_threshold
        self.report_file = Path(report_file)

    def analyze_instance(self, instance: EC2Instance) -> list[str]:
        recommendations = []

        if (
            instance.state == "running"
            and instance.running_hours_monthly >= 700
            and instance.cpu_usage < self.low_usage_threshold
        ):
            reserved_saving = instance.monthly_cost * 0.35

            recommendations.append(
                f"Instancja {instance.instance_id} działa niemal 24/7 "
                f"przy niskim użyciu CPU ({instance.cpu_usage:.1f}%). "
                f"Rozważ Reserved Instance. "
                f"Szacowana oszczędność: {reserved_saving:.2f} USD/mies."
            )

        if (
            instance.state == "stopped"
            and instance.attached_volume_gb > 0
        ):
            volume_cost = instance.attached_volume_gb * 0.08

            recommendations.append(
                f"Instancja {instance.instance_id} jest zatrzymana, "
                f"ale ma podpięty wolumen {instance.attached_volume_gb} GB. "
                f"Szacowany koszt wolumenu: {volume_cost:.2f} USD/mies."
            )

        return recommendations

    def generate_report(self, instances: list[EC2Instance]) -> None:
        lines = [
            "# Cloud Cost Optimization Report",
            "",
            "## Analiza zasobów",
            "",
        ]

        total_cost = 0.0
        recommendations_count = 0

        for instance in instances:
            total_cost += instance.monthly_cost

            lines.append(
                f"### {instance.instance_id} — {instance.instance_type}"
            )
            lines.append(f"- Stan: {instance.state}")
            lines.append(
                f"- Czas działania: {instance.running_hours_monthly} h/mies."
            )
            lines.append(f"- CPU: {instance.cpu_usage:.1f}%")
            lines.append(
                f"- Koszt miesięczny: {instance.monthly_cost:.2f} USD"
            )

            recommendations = self.analyze_instance(instance)

            if recommendations:
                lines.append("- Rekomendacje:")

                for recommendation in recommendations:
                    lines.append(f"  - {recommendation}")
                    recommendations_count += 1
            else:
                lines.append("- Rekomendacje: brak")

            lines.append("")

        lines.extend(
            [
                "## Podsumowanie",
                "",
                f"- Łączny koszt: {total_cost:.2f} USD/mies.",
                f"- Liczba rekomendacji: {recommendations_count}",
            ]
        )

        self.report_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        print("=== CLOUD COST OPTIMIZER ===")
        print(f"Łączny koszt: {total_cost:.2f} USD")
        print(f"Rekomendacje: {recommendations_count}")
        print(f"[OK] Raport zapisano: {self.report_file}")


if __name__ == "__main__":
    instances = [
        EC2Instance(
            instance_id="i-web-001",
            instance_type="t3.medium",
            state="running",
            running_hours_monthly=720,
            cpu_usage=12.0,
            monthly_cost=85.0,
        ),
        EC2Instance(
            instance_id="i-worker-002",
            instance_type="t3.small",
            state="running",
            running_hours_monthly=360,
            cpu_usage=68.0,
            monthly_cost=40.0,
        ),
        EC2Instance(
            instance_id="i-old-003",
            instance_type="t3.micro",
            state="stopped",
            running_hours_monthly=0,
            cpu_usage=0.0,
            monthly_cost=0.0,
            attached_volume_gb=100,
        ),
    ]

    optimizer = CloudCostOptimizer(
        low_usage_threshold=20.0,
    )

    optimizer.generate_report(instances)