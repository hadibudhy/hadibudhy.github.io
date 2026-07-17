"use client";

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export interface ProjectMeta {
  title: string;
  excerpt: string;
  date: string;
  tags?: string[];
  categories?: string;
}

interface ProjectCardProps {
  slug: string;
  meta: ProjectMeta;
  index?: number;
}

export function ProjectCard({ slug, meta, index = 0 }: ProjectCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Link href={`/projects/${slug}`} className="group block h-full">
        <article className="flex h-full flex-col justify-between rounded-xl border border-border bg-card/50 p-6 transition-all hover:bg-card hover:shadow-lg hover:shadow-primary/5 hover:-translate-y-1">
          <div>
            <div className="mb-4 flex flex-wrap gap-2">
              {meta.tags?.slice(0, 3).map((tag) => (
                <Badge key={tag} variant="secondary" className="text-[10px] uppercase tracking-wider">
                  {tag}
                </Badge>
              ))}
            </div>
            <h3 className="mb-2 text-xl font-bold tracking-tight text-foreground group-hover:text-primary transition-colors">
              {meta.title}
            </h3>
            <p className="text-sm leading-relaxed text-muted-foreground line-clamp-3">
              {meta.excerpt}
            </p>
          </div>
          
          <div className="mt-6 flex items-center text-sm font-medium text-primary">
            <span>Read case study</span>
            <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </div>
        </article>
      </Link>
    </motion.div>
  );
}
