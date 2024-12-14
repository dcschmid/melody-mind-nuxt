import { authClient } from "~/lib/auth-client";

export const useGameScore = () => {
  const session = authClient.useSession();

  const saveGameResult = async (category: string, points: number, earnedLP: string, language: string) => {
    const userId = session.value?.data?.user?.id;
    if (!userId) {
      throw new Error("User not logged in");
    }

    try {
      await $fetch("/api/user/update-score", {
        method: "POST",
        body: {
          userId,
          pointsToAdd: points,
          newLP: earnedLP,
          category,
          language
        },
      });

      await $fetch("/api/highscore/category", {
        method: "POST",
        body: {
          userId,
          category,
          points,
          language: language,
        },
      });

      await $fetch("/api/highscore/total", {
        method: "POST",
        body: {
          userId,
          points,
          language: language,
        },
      });
    } catch (error) {
      console.error("Error saving game result:", error);
      throw error;
    }
  };

  return {
    saveGameResult,
  };
};
