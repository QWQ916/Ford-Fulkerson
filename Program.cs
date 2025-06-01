using System.Collections.Generic;
using System;
using System.ComponentModel;

public class FordFulkerson
{
    public static void Main()
    {
        // Граф, представленный матрицей смежности.
        // Значение [i, j] - пропускная способность ребра от узла i к узлу j.
        // 0 означает отсутствие ребра.
        int[,] graph = {
        //   A, B, C, D, E, F
            {0, 7, 4, 0, 0, 0},    // A (0)
            {0, 0, 4, 0, 2, 0},    // B (1)
            {0, 4, 0, 4, 8, 0},    // C (2)
            {0, 0, 0, 0, 0, 12},   // D (3)
            {0, 0, 0, 4, 0, 5},    // E (4)
            {0, 0, 0, 0, 0, 0}     // F (5)
        };

        int source = 0; // Исток (A)
        int sink = 5;   // Сток  (F)

        int maxFlow = FordFalkerson(graph, source, sink);

        Console.WriteLine($"\nМаксимальный поток: {maxFlow}");
        Console.ReadKey();
    }

    public static int FordFalkerson(int[,] graph, int source, int sink)
    {
        int n = graph.GetLength(0);
        int[,] residualGraph = new int[n, n];
        Array.Copy(graph, residualGraph, graph.Length); // Копируем исходный граф в residualGraph

        int maxFlow = 0;

        while (true)
        {
            List<int> path = DFS(residualGraph, source, sink);

            if (path == null)
            {
                break; // Нет больше увеличивающих путей
            }

            int pathFlow = int.MaxValue;
            for (int i = 0; i < path.Count - 1; i++)
            {
                pathFlow = Math.Min(pathFlow, residualGraph[path[i], path[i + 1]]);
            }

            print(path, pathFlow);

            for (int i = 0; i < path.Count - 1; i++)
            {
                residualGraph[path[i], path[i + 1]] -= pathFlow;
                residualGraph[path[i + 1], path[i]] += pathFlow;
            }

            maxFlow += pathFlow;
        }

        return maxFlow;
    }

    // Поиск в длину для поиска увеличивающего пути
    public static List<int> DFS(int[,] graph, int source, int sink)
    {
        int n = graph.GetLength(0);
        bool[] visited = new bool[n];

        // Внутренняя рекурсивная функция для поиска пути
        List<int> _dfs(int currentNode, List<int> path)
        {
            if (currentNode == sink)
            {
                return path;
            }

            visited[currentNode] = true;

            for (int v = 0; v < n; v++)
            {
                if (!visited[v] && graph[currentNode, v] > 0)
                {
                    List<int> newPath = new List<int>(path);
                    newPath.Add(v);
                    var result = _dfs(v, newPath);
                    if (result != null)
                    {
                        return result;
                    }
                }
            }

            return null; // Путь не найден из этой ветки
        }

        // Запуск рекурсивной функции с начальной точки
        return _dfs(source, new List<int>() { source });
    }

    static void print(List<int> p, int x)
    {
        Console.WriteLine();
        foreach (var v in p)
        {
            Console.Write($"{v} ");
        }
        Console.Write($" |  {x}");
        Console.WriteLine();
    }
}