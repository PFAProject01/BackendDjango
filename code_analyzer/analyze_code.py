import subprocess
from collections import defaultdict
import sys
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    import javalang
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'javalang'])
    import javalang


class JavaCodeAnalyzer:
    def __init__(self, java_code: str):
        self.code = java_code
        try:
            # Parse the Java code and build the syntax tree
            self.tree = javalang.parse.parse(java_code)
        except javalang.parser.JavaSyntaxError as e:
            raise ValueError(f"Invalid Java syntax: {e}")

    def get_coupling(self):
        """
        Detects class-level coupling by analyzing dependencies in field and method declarations.
        """
        class_relations = defaultdict(list)
        classes = [node for path, node in self.tree.filter(javalang.tree.ClassDeclaration)]

        for cls in classes:
            for body in cls.body:
                # Check for field declarations
                if isinstance(body, javalang.tree.FieldDeclaration):
                    for declarator in body.declarators:
                        class_relations[cls.name].append(declarator.name)

                # Check for method statements that use other class members
                elif isinstance(body, javalang.tree.MethodDeclaration):
                    for stmt in (body.body or []):
                        if isinstance(stmt, javalang.tree.StatementExpression) and hasattr(stmt.expression, 'member'):
                            class_relations[cls.name].append(stmt.expression.member)

        logger.debug(f"Class relations detected: {class_relations}")
        return class_relations

    def detect_coupling(self):
        class_relations = defaultdict(set)
        classes = [node for path, node in self.tree.filter(javalang.tree.ClassDeclaration)]
        for cls in classes:
            class_name = cls.name
            for body in cls.body:
                # Dépendances via les champs
                if isinstance(body, javalang.tree.FieldDeclaration):
                    for declarator in body.declarators:
                        if hasattr(body.type, 'name'):
                            dependency = body.type.name
                            class_relations[class_name].add(dependency)

                # Dépendances via les méthodes
                elif isinstance(body, javalang.tree.MethodDeclaration):
                    method_body = body.body or []
                    for stmt in method_body:
                        if isinstance(stmt, javalang.tree.MethodInvocation) and hasattr(
                                stmt.expression.qualifier, 'name'):
                            dependency = stmt.expression.qualifier.name
                            class_relations[class_name].add(dependency)

                # Dépendances via l'instanciation directe
                elif isinstance(body, javalang.tree.ConstructorDeclaration):
                    constructor_body = body.body or []
                    for stmt in constructor_body:
                        if isinstance(stmt.expression, javalang.tree.ClassCreator) and hasattr(stmt.expression.type,
                                                                                               'name'):
                            dependency = stmt.expression.type.name
                            class_relations[class_name].add(dependency)

        logger.debug(f"Coupling detected: {dict(class_relations)}")
        return {cls: list(deps) for cls, deps in class_relations.items()}

    def detect_duplication(self):
        """
        Detects duplicated lines of code in the Java source.
        """
        lines = self.code.split("\n")
        line_count = defaultdict(int)

        for line in lines:
            stripped = line.strip()
            if stripped:
                line_count[stripped] += 1

        duplicates = {line: count for line, count in line_count.items() if count > 1}
        logger.debug(f"Code duplication detected: {duplicates}")
        return duplicates

    def detect_design_patterns(self):
        """
        Identifies common design patterns in the Java code.
        """
        detected_patterns = []
        classes = [node for path, node in self.tree.filter(javalang.tree.ClassDeclaration)]
        methods = [node for path, node in self.tree.filter(javalang.tree.MethodDeclaration)]

        # Detect Singleton Pattern
        for cls in classes:
            has_private_constructor = any(
                isinstance(body, javalang.tree.ConstructorDeclaration) and 'private' in body.modifiers
                for body in cls.body
            )
            has_static_instance = any(
                isinstance(body, javalang.tree.FieldDeclaration) and 'static' in body.modifiers
                for body in cls.body
            )
            has_get_instance_method = any(
                isinstance(method,
                           javalang.tree.MethodDeclaration) and method.name.lower() == 'getinstance' and 'static' in method.modifiers
                for method in methods
            )
            if has_private_constructor and has_static_instance and has_get_instance_method:
                detected_patterns.append(f"Singleton Pattern detected in class: {cls.name}")

        # Detect Factory Pattern
        for method in methods:
            if method.body and any(
                    isinstance(stmt, javalang.tree.ReturnStatement) and hasattr(stmt, 'expression') and hasattr(
                        stmt.expression, 'type')
                    for stmt in method.body
            ):
                detected_patterns.append(f"Factory Pattern detected in method: {method.name}")

        # Detect Observer Pattern
        for method in methods:
            if (method.name.lower().startswith('add') and 'listener' in method.name.lower()) or \
                    (method.name.lower().startswith('notify') and 'listener' in method.name.lower()):
                detected_patterns.append(f"Observer Pattern detected in method: {method.name}")

        logger.debug(f"Design patterns detected: {detected_patterns}")
        return detected_patterns

    def generate_classes_based_on_patterns(self):
        """
        Generate new classes based on detected design patterns, coupling, and duplication issues.
        """
        modified_code = self.code.split('\n')  # Start with the existing code
        detected_patterns = self.detect_design_patterns()
        coupling_issues = self.get_coupling()
        duplication_issues = self.detect_duplication()

        for pattern in detected_patterns:
            if "Singleton" in pattern:
                modified_code.extend(self.generate_singleton_classes())
            elif "Factory" in pattern:
                modified_code.extend(self.generate_factory_classes())
            elif "Observer" in pattern:
                modified_code.extend(self.generate_observer_classes())

        # Handle coupling issues

        for class_name, dependencies in coupling_issues.items():
            if len(dependencies) > 2:
                modified_code.extend(self.apply_mediator_or_facade_pattern(class_name, dependencies))

        # Handle duplication issues
        if duplication_issues:
            modified_code.extend(self.refactor_duplicated_code(duplication_issues))

        return '\n'.join(modified_code)

    def generate_singleton_classes(self):
        """
        Generate Singleton classes based on detected patterns.
        """
        generated_code = [
            "public class SingletonExample {",
            "   private static SingletonExample instance;",
            "   private SingletonExample() {",
            "       // private constructor",
            "   }",
            "   public static SingletonExample getInstance() {",
            "       if (instance == null) {",
            "           instance = new SingletonExample();",
            "       }",
            "       return instance;",
            "   }",
            "}"
        ]
        return generated_code

    def generate_factory_classes(self):
        """
        Generate Factory classes based on detected patterns.
        """
        generated_code = [
            "public class FactoryExample {",
            "   public static Object createInstance(String type) {",
            "       switch (type) {",
            "           case \"type1\":",
            "               return new Type1();",
            "           case \"type2\":",
            "               return new Type2();",
            "           default:",
            "               throw new IllegalArgumentException(\"Unknown type: \" + type);",
            "       }",
            "   }",
            "}"
        ]
        return generated_code

    def generate_observer_classes(self):
        """
        Generate Observer pattern classes based on detected patterns.
        """
        generated_code = [
            "import java.util.ArrayList;",
            "import java.util.List;",
            "",
            "public class Subject {",
            "   private List<Observer> observers = new ArrayList<>();",
            "   public void addObserver(Observer observer) {",
            "       observers.add(observer);",
            "   }",
            "   public void removeObserver(Observer observer) {",
            "       observers.remove(observer);",
            "   }",
            "   public void notifyObservers() {",
            "       for (Observer observer : observers) {",
            "           observer.update();",
            "       }",
            "   }",
            "}",
            "",
            "public interface Observer {",
            "   void update();",
            "}",
            "",
            "public class ConcreteObserver implements Observer {",
            "   @Override",
            "   public void update() {",
            "       // Observer logic here",
            "   }",
            "}"
        ]
        return generated_code

    def apply_mediator_or_facade_pattern(self, class_name, dependencies):
        """
        Apply Mediator or Facade pattern based on high coupling issues.
        """
        # Example: applying a mediator pattern (stub example)
        generated_code = [
            f"public class {class_name}Mediator {{",
            f"   private {class_name} {class_name.lower()};",
            f"   public {class_name}Mediator({class_name} {class_name.lower()}) {{",
            f"       this.{class_name.lower()} = {class_name.lower()};",
            f"   }}",
            f"   // Methods to mediate interactions between {class_name} and other classes",
            f"}}"
        ]
        return generated_code

    def refactor_duplicated_code(self, duplication_issues):
        """
        Refactor duplicated code blocks using factory or strategy patterns.
        """
        generated_code = []
        for code, count in duplication_issues.items():
            # Example of refactoring duplicate code into a factory method
            generated_code.extend(self.generate_factory_classes())
        return generated_code

    def recommend_patterns(self):
        """
        Analyzes the code and provides recommendations for improvement.
        """
        recommendations = []

        # Detect high coupling
        coupling = self.get_coupling()
        if any(len(deps) > 2 for deps in coupling.values()):
            recommendations.append("High coupling detected. Use Facade or Mediator to reduce dependencies.")

        # Detect code duplication
        duplication = self.detect_duplication()
        if duplication:
            recommendations.append(
                "Code duplication detected. Consider refactoring using Factory or Strategy patterns.")

        # Include detected design patterns
        detected_patterns = self.detect_design_patterns()
        recommendations.extend(detected_patterns)

        logger.info(f"Recommendations: {recommendations}")
        return recommendations